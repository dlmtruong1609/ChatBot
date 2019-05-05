from datetime import datetime
from chatterbot.logic.logic_adapter import LogicAdapter
from chatterbot.conversation import Statement


class TimeLogicAdapterVN(LogicAdapter):
    """
    The TimeLogicAdapter returns the current time.

    :kwargs:
        * *positive* (``list``) --
          The time-related questions used to identify time questions.
          Defaults to a list of English sentences.
        * *negative* (``list``) --
          The non-time-related questions used to identify time questions.
          Defaults to a list of English sentences.
    """

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        from nltk import NaiveBayesClassifier

        self.positive = kwargs.get('positive', [
            'Mấy giờ rồi',
            'Hiện tại là mấy giờ',
            'Bạn có biết bây giờ là mấy giờ',
            'Cho mình hỏi bây giờ là mấy giờ',
            'Hiện giờ hiện tại',
            'what is the time'
        ])

        self.negative = kwargs.get('negative', [
            'Đến giờ đi ngủ rồi',
            'Màu sắc yêu thích của bạn là gì',
            'Tôi đã có khoảng thời gian tuyệt với',
            'cỏ xạ hương là loại thảo mộc yêu thích của tôi',
            'bạn có thời gian để xem bài luận của tôi không',
            'làm thế nào để bạn có thời gian để làm tất cả điều này'
            'nó là gì',
            'ljanwlglwa'
        ])

        labeled_data = (
            [
                (name, 0) for name in self.negative
            ] + [
                (name, 1) for name in self.positive
            ]
        )

        train_set = [
            (self.time_question_features(text), n) for (text, n) in labeled_data
        ]

        self.classifier = NaiveBayesClassifier.train(train_set)

    def time_question_features(self, text):
        """
        Provide an analysis of significant features in the string.
        """
        features = {}

        # A list of all words from the known sentences
        all_words = " ".join(self.positive + self.negative).split()

        # A list of the first word in each of the known sentence
        all_first_words = []
        for sentence in self.positive + self.negative:
            all_first_words.append(
                sentence.split(' ', 1)[0]
            )

        for word in text.split():
            features['first_word({})'.format(word)] = (word in all_first_words)

        for word in text.split():
            features['contains({})'.format(word)] = (word in all_words)


        return features

    def process(self, statement, additional_response_selection_parameters=None):
        now = datetime.now()

        time_features = self.time_question_features(statement.text.lower())
        confidence = self.classifier.classify(time_features)
        response = Statement(text='Bây giờ là ' + now.strftime('%I:%M %p'))

        response.confidence = confidence
        return response
