class Classification:
    def __init__(self, lexical_category, features):
        self._lexical_category = lexical_category
        self._features = features
        self._length_features = len(features)


    def get_lexical_category(self):
        return self._lexical_category

    def get_feature(self, key_feature):
        if not key_feature in self._features:
            return None

        return self._features[key_feature]

    def get_type_features(self):
        return self._features.keys()

    def get_features(self):
        return self._features.values()


    def get_size_features(self):
        return self._length_features