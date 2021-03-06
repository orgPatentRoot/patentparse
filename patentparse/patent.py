import json
import patentparse
import xml.etree.cElementTree


class Patent(object):
    def __init__(self, raw):
        self._raw = raw
        self._tree = None
        if self.tree.get('id') != 'us-patent-grant':
            raise patentparse.PatentParsingException(
                "Not a patent XML element")

    @property
    def tree(self):
        if self._tree:
            return self._tree
        self._tree = xml.etree.cElementTree.fromstring(self._raw)
        return self._tree

    @property
    def invention_title(self):
        return self.tree.find('.//invention-title').text

    @property
    def claims(self):
        claims = self.tree.findall('.//claim')
        for claim in claims:
            yield xml.etree.cElementTree.tostring(
                claim, method='text', encoding='utf-8')

    @property
    def doc_number(self):
        return self.tree.find('.//publication-reference//doc-number').text

    @property
    def json(self):
        return json.dumps(dict(
            doc_number=self.doc_number,
            invention_title=self.invention_title,
            claims=list(self.claims),
            ))
