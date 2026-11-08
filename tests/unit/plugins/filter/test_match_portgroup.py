"""Unit tests for the match_portgroup filter plugin."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import importlib.util
import pathlib

import pytest

ANNOTATION = "infra.openshift-virtualization-migration/source-portgroup"

# The collection is not necessarily importable as
# ansible_collections.infra.openshift_virtualization_migration when running
# pytest from the repository root, so load the plugin straight from its path.
_PLUGIN_PATH = (
    pathlib.Path(__file__).resolve().parents[4] / "plugins" / "filter" / "match_portgroup.py"
)
_SPEC = importlib.util.spec_from_file_location("match_portgroup", _PLUGIN_PATH)
_MODULE = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_MODULE)

match_portgroup = _MODULE.match_portgroup
FilterModule = _MODULE.FilterModule


def nad(name, namespace="default", portgroup=None, annotations=None):
    """Build a minimal Forklift inventory NAD entry."""
    if annotations is None:
        annotations = {} if portgroup is None else {ANNOTATION: portgroup}
    return {
        "object": {
            "metadata": {
                "name": name,
                "namespace": namespace,
                "annotations": annotations,
            }
        }
    }


def names(nads):
    """Return the NAD names of a filter result, for readable assertions."""
    return [item["object"]["metadata"]["name"] for item in nads]


class TestSinglePortgroup:
    """A NAD annotated with exactly one portgroup."""

    def test_matches_exact_name(self):
        nads = [nad("nad-a", portgroup="VLAN100")]
        assert names(match_portgroup(nads, "VLAN100", ANNOTATION)) == ["nad-a"]

    def test_does_not_match_other_name(self):
        nads = [nad("nad-a", portgroup="VLAN100")]
        assert match_portgroup(nads, "VLAN200", ANNOTATION) == []

    def test_match_is_case_sensitive(self):
        nads = [nad("nad-a", portgroup="VLAN100")]
        assert match_portgroup(nads, "vlan100", ANNOTATION) == []

    def test_does_not_match_substring(self):
        nads = [nad("nad-a", portgroup="VLAN1000")]
        assert match_portgroup(nads, "VLAN100", ANNOTATION) == []

    def test_surrounding_whitespace_is_ignored(self):
        nads = [nad("nad-a", portgroup="  VLAN100  ")]
        assert names(match_portgroup(nads, "VLAN100", ANNOTATION)) == ["nad-a"]

    def test_selects_only_matching_nads(self):
        nads = [
            nad("nad-a", portgroup="VLAN100"),
            nad("nad-b", portgroup="VLAN200"),
            nad("nad-c", portgroup="VLAN100"),
        ]
        assert names(match_portgroup(nads, "VLAN100", ANNOTATION)) == ["nad-a", "nad-c"]


class TestMultiplePortgroups:
    """A NAD annotated with a comma-separated list of portgroups."""

    @pytest.mark.parametrize("network_name", ["VLAN100", "VLAN200", "VLAN300"])
    def test_matches_any_listed_portgroup(self, network_name):
        nads = [nad("shared", portgroup="VLAN100,VLAN200,VLAN300")]
        assert names(match_portgroup(nads, network_name, ANNOTATION)) == ["shared"]

    def test_tolerates_spaces_around_separators(self):
        nads = [nad("shared", portgroup="VLAN100 , VLAN200 ,VLAN300")]
        assert names(match_portgroup(nads, "VLAN200", ANNOTATION)) == ["shared"]

    def test_ignores_empty_entries(self):
        nads = [nad("shared", portgroup="VLAN100,,  ,VLAN200,")]
        assert names(match_portgroup(nads, "VLAN200", ANNOTATION)) == ["shared"]
        assert match_portgroup(nads, "", ANNOTATION) == []

    def test_does_not_match_unlisted_portgroup(self):
        nads = [nad("shared", portgroup="VLAN100,VLAN200")]
        assert match_portgroup(nads, "VLAN300", ANNOTATION) == []

    def test_does_not_match_whole_annotation_value(self):
        nads = [nad("shared", portgroup="VLAN100,VLAN200")]
        assert match_portgroup(nads, "VLAN100,VLAN200", ANNOTATION) == []

    def test_portgroup_name_containing_comma_never_matches(self):
        # Documented limitation: the comma is always a separator.
        nads = [nad("odd", portgroup="VLAN100,VLAN200")]
        assert match_portgroup(nads, "VLAN100,VLAN200", ANNOTATION) == []


class TestNamespaceFiltering:
    """The optional namespace argument."""

    @pytest.fixture
    def nads(self):
        return [
            nad("nad-a", namespace="ns-a", portgroup="VLAN100"),
            nad("nad-b", namespace="ns-b", portgroup="VLAN100"),
        ]

    def test_restricts_results_to_namespace(self, nads):
        result = match_portgroup(nads, "VLAN100", ANNOTATION, "ns-b")
        assert names(result) == ["nad-b"]

    def test_no_results_for_unknown_namespace(self, nads):
        assert match_portgroup(nads, "VLAN100", ANNOTATION, "ns-c") == []

    @pytest.mark.parametrize("namespace", ["", "   ", None])
    def test_blank_namespace_disables_filtering(self, nads, namespace):
        if namespace is None:
            result = match_portgroup(nads, "VLAN100", ANNOTATION)
        else:
            result = match_portgroup(nads, "VLAN100", ANNOTATION, namespace)
        assert names(result) == ["nad-a", "nad-b"]

    def test_namespace_argument_is_trimmed(self, nads):
        result = match_portgroup(nads, "VLAN100", ANNOTATION, "  ns-a  ")
        assert names(result) == ["nad-a"]

    def test_namespace_and_portgroup_must_both_match(self, nads):
        assert match_portgroup(nads, "VLAN200", ANNOTATION, "ns-a") == []


class TestNoMatch:
    """Inputs that legitimately yield no match."""

    def test_empty_input_list(self):
        assert match_portgroup([], "VLAN100", ANNOTATION) == []

    def test_nad_without_annotations(self):
        assert match_portgroup([nad("nad-a")], "VLAN100", ANNOTATION) == []

    def test_nad_with_other_annotations_only(self):
        nads = [nad("nad-a", annotations={"other/annotation": "VLAN100"})]
        assert match_portgroup(nads, "VLAN100", ANNOTATION) == []

    def test_empty_annotation_value(self):
        nads = [nad("nad-a", portgroup="")]
        assert match_portgroup(nads, "VLAN100", ANNOTATION) == []

    def test_different_annotation_key(self):
        nads = [nad("nad-a", portgroup="VLAN100")]
        assert match_portgroup(nads, "VLAN100", "other/annotation") == []


class TestMalformedInput:
    """Entries that do not have the expected shape are skipped, not fatal."""

    @pytest.mark.parametrize(
        "entry",
        [
            {},
            {"object": {}},
            {"object": {"metadata": {}}},
            {"object": None},
            {"object": {"metadata": None}},
            {"object": {"metadata": {"annotations": None}}},
            {"object": {"metadata": {"annotations": "not-a-dict"}}},
            "a string",
            None,
            42,
            [],
        ],
    )
    def test_malformed_entry_is_skipped(self, entry):
        assert match_portgroup([entry], "VLAN100", ANNOTATION) == []

    def test_malformed_entries_do_not_hide_valid_ones(self):
        nads = [
            {"object": {"metadata": {}}},
            None,
            nad("nad-a", portgroup="VLAN100"),
            "a string",
            nad("nad-b", portgroup="VLAN100,VLAN200"),
        ]
        assert names(match_portgroup(nads, "VLAN100", ANNOTATION)) == ["nad-a", "nad-b"]

    def test_non_string_annotation_value_is_skipped(self):
        nads = [nad("nad-a", annotations={ANNOTATION: ["VLAN100"]})]
        assert match_portgroup(nads, "VLAN100", ANNOTATION) == []

    def test_malformed_namespace_entry_is_skipped(self):
        nads = [
            {
                "object": {
                    "metadata": {
                        "name": "nad-a",
                        "annotations": {ANNOTATION: "VLAN100"},
                    }
                }
            }
        ]
        # No namespace key: the NAD cannot belong to the requested namespace.
        assert match_portgroup(nads, "VLAN100", ANNOTATION, "ns-a") == []


class TestResultShape:
    """The filter returns the original objects, unmodified."""

    def test_returns_original_objects(self):
        entry = nad("nad-a", portgroup="VLAN100")
        result = match_portgroup([entry], "VLAN100", ANNOTATION)
        assert result[0] is entry

    def test_preserves_input_order(self):
        nads = [nad("nad-%d" % i, portgroup="VLAN100") for i in range(5)]
        result = match_portgroup(nads, "VLAN100", ANNOTATION)
        assert names(result) == ["nad-0", "nad-1", "nad-2", "nad-3", "nad-4"]

    def test_does_not_mutate_input(self):
        nads = [nad("nad-a", portgroup="VLAN100"), nad("nad-b", portgroup="VLAN200")]
        before = [dict(item) for item in nads]
        match_portgroup(nads, "VLAN100", ANNOTATION)
        assert nads == before


class TestFilterModule:
    """The plugin exposes the filter under the expected name."""

    def test_exposes_match_portgroup(self):
        filters = FilterModule().filters()
        assert filters == {"match_portgroup": match_portgroup}
