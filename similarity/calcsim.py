
import math
from lrucache import lru_cache

class Term:
    def __init__(self, termid, termfreq):
        self.termid = termid
        self.termfreq = termfreq
        self.tfidf = 0.0

class Doc:
    def __init__(self, docid):
        self.docid = docid

def idf(docFreq, numDocs):    
    return math.log(numDocs*1.0/(docFreq+1.0)) + 1.0

def tf(termFreq):
    return math.sqrt(termFreq)

def print_result(doc1, doc2, result):
    #print "result for ", doc1, " and ", doc2, " is ", result
    pass

def print_doc_info(doc, input):
    #print "doc ", doc
    #for eachd in input[doc]:
    #    print "\tterm" , input[doc][eachd].termid, input[doc][eachd].termfreq
    pass

class SimCalc:
    def __init__(self, input):        
        self.input = input        
        self.inputlen = len(self.input)
        self.index = {}
        self.sigmapow = {}
        print "creating invert index ...."
        self.invert_index()
        print "calcing tf&idf ...."
        self.calc_tfidf()
        print "calcing sigma pow ...."
        self.calc_sigmapow()
    
    def invert_index(self):
        for eachi in self.input:
            for eacht in self.input[eachi]:
                self.index[eacht] = self.index.get(eacht, 0) + 1
    
    def calc_tfidf(self):
        for eachi in self.input:
            for eacht in self.input[eachi]:
                self.input[eachi][eacht].tfidf = self.tfidf(self.input[eachi][eacht])
    
    def calc_sigmapow(self):
        for eachi in self.input:
            self.sigmapow[eachi] = 0.0
            for eacht in self.input[eachi]:
                self.sigmapow[eachi] += math.pow(self.input[eachi][eacht].tfidf, 2)
                
    def df(self, termid):
        return self.index[termid]
        
    def tfidf(self, term):
        return tf(term.termfreq) * idf(self.df(term.termid), self.inputlen)
                    
    def calc_doc_sim(self, doc1, doc2):
        sigma_t1t2 = 0.0
        sigma_t1 = self.sigmapow[doc1]
        sigma_t2 = self.sigmapow[doc2]
        for term1 in self.input[doc1]:
            if self.input[doc2].has_key(term1):
                sigma_t1t2 += self.input[doc1][term1].tfidf * self.input[doc2][term1].tfidf
        if sigma_t1t2 < 0.00001:
            result = 0
        else:
            result = sigma_t1t2 / (math.sqrt(sigma_t1) * math.sqrt(sigma_t2))
        print_result(doc1, doc2, result)
        return result
    
    def calc_sim(self, maxlen=100):
        # init result set
        output = {}
        inter = {}
        for eachi in self.input:
            output[eachi] = {}
            inter[eachi] = {}
                
        # calc results
        for eachi in self.input:
            print "calcing for %d" % eachi
            print_doc_info(eachi, self.input)
            for eachj in self.input:
                if eachi < eachj:
                    result = self.calc_doc_sim(eachi, eachj)
                    inter[eachi][eachj] = result
                    inter[eachj][eachi] = result
            
        # sorting and filter result    
        for eachi in self.input:
            print "filtering&sorting for %d" % eachi
            output[eachi] = sorted( filter(lambda x:x[1]>0.0001, inter[eachi].items()), lambda x,y:cmp(y[1],x[1]))[:maxlen]
            
        return output

def run(argv):
    from hbtv.content.models import Article
    from hbtv.topic.models import ArticleClass, Topic
    
    from django.core.cache import cache
    
    dt = {}
    print "loading data from db"
    for t in Topic.objects.all():
        dt2 = {}
        for a in Article.objects.filter(classifies=t.tag):
            dt2[a.id] = Term(a.id, 1 )
        dt[t.id] = dt2
    print "starting calculate"
    r = SimCalc(dt).calc_sim(100)

    for a in r:
        cache.set('tagcloud_%d' % a, r[a])

"""        
def gen_html(stag, tags, steps):    
    if tags:
        new_thresholds, results = [], []
        temp = [tag[1] for tag in tags]
        max_weight = float(max(temp))
        min_weight = float(min(temp))
        new_delta = (max_weight - min_weight)/float(steps)
        for i in range(steps + 1):
            new_thresholds.append((100 * math.log((min_weight + i * new_delta) + 2), i))
        for tag in tags:
            font_set = False
            for threshold in new_thresholds[1:int(steps)+1]:
                if (100 * math.log(tag.count + 2)) <= threshold[0] and not font_set:
                    tag.font_size = threshold[1]
                    font_set = True
"""    
    
if __name__ == '__main__':   
    t1 = Term(1, 1)
    t2 = Term(2, 1)
    t3 = Term(3, 1)
    t4 = Term(4, 1)
    t5 = Term(5, 1)
    
    test_input = {
              1 : { t1.termid: t1, 
                         t4.termid: t4 },
              2 : { 1: Term(1,1), 
                         2: Term(2,1), 
                         4: Term(4,1)},
              3 : { 3: Term(3,1), 
                         4: Term(4,1)},
              4 : { 3: Term(3,1), 
                        4: Term(4,1)},
              5 : { 1: Term(1,1), 
                         5: Term(5,1)}
              }

    #SimCalc(test_input).invert_index()
    print SimCalc(test_input).calc_sim(3)
    #print calc_sim(test_input, 2)
        