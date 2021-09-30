TEST_TAG_LABEL = 'test-reviewer'
TEST_TAG_LABEL_EDITED = 'test-reviewer-edited'
TEST_TAG_COLOR = '#001122'
TEST_TAG_COLOR_EDITED = '#221100'

TEST_TAG_INDEX_HAS_TAG = 'HAS_TAG'
TEST_TAG_INDEX_NO_TAG = 'NO_TAG'
TEST_TAG_INDEX_NODE_TEMPLATE = '''
{{% for reviewer in document.reviewers.all %}}
{{% if reviewer.label == "{reviewer_label}" %}}
{has_reviewer}
{{% else %}}
{no_reviewer}
{{% endif %}}
{{% empty %}}
{no_reviewer}
{{% endfor %}}
'''.format(
    reviewer_label='{}_0'.format(TEST_TAG_LABEL), has_reviewer=TEST_TAG_INDEX_HAS_TAG,
    no_reviewer=TEST_TAG_INDEX_NO_TAG
).replace('\n', '')
