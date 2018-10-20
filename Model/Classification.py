TYPE = 0
TEXT = 1
class Classification:
    def __init__(self, lexical_category, features):
        self._lexical_category = lexical_category
        self._features = features
        self._length_features = len(features)


    def get_lexical_category(self):
        return self._lexical_category

    def get_feature(self, id_feature):
        if (id_feature > self._length_features -1) or (id_feature < 0):
            return None

        return self._features[id_feature][TYPE], self._features[id_feature][TEXT]

    def get_type_feature(self, id_feature):
        if (id_feature > self._length_features -1) or (id_feature < 0):
            return None

        return self._features[id_feature][TYPE]

    def get_feature_text(self, id_feature):
        if (id_feature > self._length_features -1) or (id_feature < 0):
            return None

        return self._features[id_feature][TEXT]


    def get_size_features(self):
        return self._length_features