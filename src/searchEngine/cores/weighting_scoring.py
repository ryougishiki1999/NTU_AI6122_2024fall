import math

from whoosh.scoring import WeightingModel, BaseScorer


def stars_expontial_score(stars):
    a = 2.5  # 2.5 is the average stars
    b = math.e
    weighting = a * (b ** (int(stars) - a))
    return weighting


class ReviewWeighting(WeightingModel):
    def scorer(self, searcher, fieldname, text, qf=1):
        return ReviewScorer(searcher, fieldname, text, qf)

    def __str__(self):
        return "ReviewWeighting"


class ReviewScorer(BaseScorer):
    def __init__(self, searcher, fieldname, text, qf=1):
        self.searcher = searcher
        self.fieldname = fieldname
        self.text = text
        self.qf = qf

    def score(self, matcher):
        docnum = matcher.id()
        doc = self.searcher.stored_fields(docnum)
        stars_score = stars_expontial_score(float(doc.get('stars', 0)))
        relevance_score = matcher.weight()
        return stars_score * relevance_score

    def max_quality(self):
        return float('inf')


class BusinessWeighting(WeightingModel):
    def scorer(self, searcher, fieldname, text, qf=1):
        return BusinessScorer(searcher, fieldname, text, qf)

    def __str__(self):
        return "BusinessWeighting"


class BusinessScorer(BaseScorer):

    def __init__(self, searcher, fieldname, text, qf=1):
        self.searcher = searcher
        self.fieldname = fieldname
        self.text = text
        self.qf = qf

    def score(self, matcher):
        docnum = matcher.id()
        doc = self.searcher.stored_fields(docnum)
        stars_score = stars_expontial_score(float(doc.get('stars', 0)))
        relevance_score = matcher.weight()
        review_count_score = math.log(int(doc.get('review_count', 0)) + 1, 10)
        return stars_score * relevance_score * review_count_score

    def max_quality(self):
        return float('inf')
