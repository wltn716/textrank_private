from newspaper import Article
from konlpy.tag import Kkma
from konlpy.tag import Twitter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import normalize
import numpy as np
import requests
from bs4 import BeautifulSoup
from threading import Thread
import jpype
import sys
import re
regex = r'[가-힣]+'

twit = Twitter()
kkma = Kkma()

class SentenceTokenizer(object):
    def __init__(self):
        self.kkma = kkma
        self.twitter = twit
        self.stopwords = ['중인' ,'만큼', '마찬가지', '꼬집었', "연합뉴스", "데일리", "동아일보", "중앙일보", "조선일보", "기자"
        ,"아", "휴", "아이구", "아이쿠", "아이고", "어", "나", "우리", "저희", "따라", "의해", "을", "를", "에", "의", "가","억원","원장","때문","가","@"
        ,"권혜민","이유지","인턴","측은","중앙","대해","면서","노컷뉴스"]
    
    def url2sentences(self,url):
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, 'lxml')
        daum = soup.select('section > p')
        daum2 = soup.select("section > div")
        naver = soup.findAll("div",id="articleBodyContents")
        naver_enter = soup.findAll("div",id="articeBody")
        naver_sports = soup.findAll("div",id="newsEndContents")
        
        self.origin_text=[]
        text=''
        sentences=[]
        temp = []
        
        for sent in daum2:
            text = sent.text
            temp.extend(text.split("."))
        
        for sent in daum:
            text = sent.text
            temp.extend(text.split(". "))
               
        for sent in naver:
            for unused in soup.findAll("a"):
                unused.decompose()
            for unused in soup.findAll("script"):
                unused.decompose()
            for unused in soup.findAll("span"):
                unused.replace_with('')
            for unused in soup.findAll("p"):
                unused.decompose()
            for unused in soup.findAll("strong"):
                unused.decompose()
            for unused in soup.findAll("br"):
                unused.replace_with('. ')

            text = sent.get_text()
            temp.extend(text.split('. '))


               
        for sent in naver_enter:
            for unused in soup.findAll("a"):
                unused.decompose()
            for unused in soup.findAll("script"):
                unused.decompose()
            for unused in soup.findAll("span"):
                unused.replace_with('')
            for unused in soup.findAll("p"):
                unused.decompose()
            for unused in soup.findAll("br"):
                unused.replace_with('. ')
            text = sent.get_text()
            temp.extend(text.split('. '))

        for sent in naver_sports:
            for unused in soup.findAll("a"):
                unused.decompose()
            for unused in soup.findAll("script"):
                unused.decompose()
            for unused in soup.findAll("span"):
                unused.replace_with('')
            for unused in soup.findAll("p"):
                unused.decompose()
            for unused in soup.findAll("br"):
                unused.replace_with('. ')
            text = sent.get_text()
            temp.extend(text.split('. '))

        sentences = self.makeSentences(temp)

        return sentences
    
    def text2sentences(self, text):
        jpype.attachThreadToJVM()
        temp = text.split(". ")
        
        sentences = self.makeSentences(temp)

        return sentences

    def makeSentences(self, temp):
        idx_r = []
        a=0

        for sent in temp:
            self.origin_text.append(sent)

        for idx in range(0,len(temp)):
            if not re.findall(regex,temp[idx]):
                idx_r.append(idx-a)
                a+=1

        for idx in idx_r:
            temp.pop(idx)

        sentences = temp

        for s in sentences[:]:
            if "@" in s:
                sentences.remove(s)   

        for idx in range(0, len(sentences)):
            if len(sentences[idx]) <= 10:
                sentences[idx-1] += (' ' + sentences[idx])
                sentences[idx] = ''

        #공백인 원소 제거
        for idx in sentences[:]:
            if len(idx) > 0:
                if idx[-1]!='다':
                    if idx[-1]!='.':
                        sentences.remove(idx)  

        print(sentences)

<<<<<<< HEAD
=======

>>>>>>> shinah
        return sentences    

    
    def get_nouns(self, sentences):
        nouns = []
        jpype.attachThreadToJVM()
        for sentence in sentences:
            if sentence is not '':
                nouns.append(' '.join([noun for noun in self.twitter.nouns(str(sentence))
                                       if noun not in self.stopwords and len(noun) > 1]))
        return nouns
    
class GraphMatrix(object):
    def __init__(self):
        self.tfidf = TfidfVectorizer()
        self.cnt_vec = CountVectorizer()
        self.graph_sentence = []
        
    def build_sent_graph(self, sentence):
        cnt_vec_mat = normalize(self.cnt_vec.fit_transform(sentence).toarray().astype(float), axis=0)
        a = 0
        
        while 1>0:
            for element in range(len(cnt_vec_mat[a])):
                cnt_vec_mat[a][element]+= 0.5

            a += 1
            if a == len(cnt_vec_mat)-1:
                break
            
        for element in range(cnt_vec_mat.shape[0]):
            cnt_vec_mat[0][element] *= 2
            
        self.graph_sentence = np.dot(cnt_vec_mat, cnt_vec_mat.T)
        
        #for element in range(self.graph_sentence.shape[0]):s
        #   self.graph_sentence[0][element] *= 2
            
        return self.graph_sentence
    
    def build_words_graph(self, sentence):
        cnt_vec_mat = normalize(self.cnt_vec.fit_transform(sentence).toarray().astype(float), axis=0)
        vocab = self.cnt_vec.vocabulary_
        for row in range(len(cnt_vec_mat)):
            for element in range(len(cnt_vec_mat[row])):
                cnt_vec_mat[row][element] += 1

        for element in range(cnt_vec_mat.shape[0]):
            cnt_vec_mat[0][element] *= 2

        return np.dot(cnt_vec_mat.T, cnt_vec_mat), {vocab[word] : word for word in vocab}
    
class Rank(object):
    def get_ranks(self, graph, d=0.85): # d = damping factor
        A = graph
        matrix_size = A.shape[0]
        for id in range(matrix_size):
            A[id, id] = 0 # diagonal 부분을 0으로
            link_sum = np.sum(A[:,id]) # A[:, id] = A[:][id]
        if link_sum != 0:
            A[:, id] /= link_sum
        A[:, id] *= -d
        A[id, id] = 1
        
        B = (1-d) * np.ones((matrix_size, 1))
        ranks = np.linalg.solve(A, B) # 연립방정식 Ax = b
        ranks[0]*=2
        return {idx: r[0] for idx, r in enumerate(ranks)}
    
class TextRank(object):
    def __init__(self, text):
        self.sent_tokenize = SentenceTokenizer()
        if text[:5] in ('http:', 'https'):
            self.sentences = self.sent_tokenize.url2sentences(text)
        else:
            self.sentences = self.sent_tokenize.text2sentences(text)
                   
        self.nouns = self.sent_tokenize.get_nouns(self.sentences)
        print(self.nouns)
        
        self.graph_matrix = GraphMatrix()
        self.sent_graph = self.graph_matrix.build_sent_graph(self.nouns)
        self.words_graph, self.idx2word = self.graph_matrix.build_words_graph(self.nouns)
        
        self.rank = Rank()
        self.sent_rank_idx = self.rank.get_ranks(self.sent_graph)
        self.sorted_sent_rank_idx = sorted(self.sent_rank_idx, key=lambda k: self.sent_rank_idx[k], reverse=True)

        self.word_rank_idx =  self.rank.get_ranks(self.words_graph)
        self.sorted_word_rank_idx = sorted(self.word_rank_idx, key=lambda k: self.word_rank_idx[k], reverse=True)
        
    def summarize(self, sent_num=3):
        summary = []
        index=[]
        for idx in self.sorted_sent_rank_idx[:sent_num]:
            index.append(idx)
        
        index.sort()
        for idx in index:
            self.sentences[idx]=self.sentences[idx].strip()
            summary.append(self.sentences[idx])
        
        return summary
        
    def keywords(self, word_num=10):
        rank = Rank()
        rank_idx = rank.get_ranks(self.words_graph)
        sorted_rank_idx = sorted(rank_idx, key=lambda k: rank_idx[k], reverse=True)
        
        keywords = []
        index=[]
        for idx in sorted_rank_idx[:word_num]:
            index.append(idx)
            
        for idx in index:
            keywords.append(self.idx2word[idx])
        
        return keywords
