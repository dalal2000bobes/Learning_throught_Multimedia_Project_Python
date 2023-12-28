import stanza 
import random 
import re
import gensim
import nltk
import numpy as np
from nltk import ngrams
from nltk.stem.isri import ISRIStemmer
from transformers import AutoTokenizer,AutoModelForSeq2SeqLM

ner_stanza = stanza.Pipeline(lang='ar', processors='tokenize,ner')
modell=gensim.models.Word2Vec.load("Files/Models/full_grams_cbow_300_twitter.mdl")  # بتحطي مسار ملف بعتلك ياه
model = AutoModelForSeq2SeqLM.from_pretrained("Mihakram/AraT5-base-question-generation")
tokenizer = AutoTokenizer.from_pretrained("Mihakram/AraT5-base-question-generation")

def split_sentences(text):
    """ Simple Arabic tokenizer and sentencizer. It is a space-based tokenizer. I use some rules to handle
    tokenition exception like words containing the preposition 'و'. For example 'ووالدته' is tokenized to 'و والدته'
    :param text: Arabic text to handle
    :return: list of tokenized sentences
    """
    try:
        text = text.decode('utf-8')
    except(UnicodeDecodeError, AttributeError):
        pass
    text = text.strip()
    tokenizer_exceptions = ["وظف", "وضعها", "وضعه", "وقفنا", "وضع", "وصفوها", "وجهوا", "وجهتها", "وول", "وطننا",
                            "وكالته", "وجع", "والدته", "والده", "وطره", "وادي", "وضعية", "وعدوا",
                            "واجهات", "وفرتها", "وقاية", "وفا", "وزيرنا", "وزارتي", "وجهاها", "واردة", "وضعته",
                            "وزارية",
                            "وضعتها", "وافته", "وجاهة", "وهمية", "واجهة", "واضعاً", "واقعي", "ودائع", "واعدا", "واع",
                            "واسعا", "ولاة",
                            "ورائها", "وحدها", "وزارتي", "وزارتي", "والدة", "وزرائها", "وسطاء", "وليامز", "وافق",
                            "والدها", "واضعين", "وسم", "وافق", "وجهها", "واسعة", "واسع", "وزنها", "وزنه", "وصايته",
                            "وصلوا", "والدها", "وصولاً", "وضوحاً", "وجّهته", "وضعته", "ويكيليكس", "وحدها", "وزيراً",
                            "والي",
                            "وقفات", "وعر", "واقيًا", "وقوف", "وصولهم", "وارسو", "واجهت", "وقائية", "وضعهم",
                            "وسطاء", "وظيفته", "ورائه", "واسع", "ورط", "وظفت", "وقوف", "وافقت", "وفدًا", "وصلتها",
                            "وثائقي", "ويليان", "وساط", "وُقّع", "وَقّع", "وخيمة", "ويست", "والتر", "وهران", "ولاعة",
                            "ولايت", "والي", "واجب", "وظيفتها", "ولايات", "واشنطن", "واصف",
                            "وقح", "وعد", "وقود", "وزن", "وقوع", "ورشة", "وقائع", "وتيرة", "وساطة", "وفود", "وفات",
                            "وصاية", "وشيك", "وثائق", "وطنية", "وجهات", "وجهت", "وعود", "وضعهم", "وون", "وسعها", "وسعه",
                            "ولاية", "واصفاً", "واصلت", "وليان", "وجدتها", "وجدته", "وديتي", "وطأت", "وطأ", "وعودها",
                            "وجوه", "وضوح", "وجيز", "ورثنا", "ورث", "واقع", "وهم", "واسعاً", "وراثية", "وراثي", "والاس",
                            "واجهنا", "وابل", "ويكيميديا", "واضحا", "واقف", "واضح", "وصفته", "واتساب", "وحدات", "ون",
                            "وورلد", "والد", "وكلاء", "وتر", "وثيق", "وكالة", "وكالات", "و احدة", "واحد", "وصيته",
                            "وصيه", "ويلمينغتون", "ولد", "وزر", "وعي", "وفد", "وصول", "وقف", "وفاة", "ووتش", "وسط",
                            "وزراء", "وزارة", "ودي", "وصيف", "ويمبلدون", "وست", "وهمي", "وهج", "وهميا", "والد", "وليد",
                            "وثار",
                            "وجد", "وجه", "وقت", "ويلز", "وجود", "وجيه", "وحد", "وحيد", "ودا", "وداد", "ودرو",
                            "ودى", "وديع", "وراء", "ورانس", "ورث", "ورَّث", "ورد", "وردة", "ورق", "ورم", "وزير",
                            "وسام", "وسائل", "وستون", "وسط", "وسن", "وسيط", "وسيلة", "وسيم", "وصاف", "وصف", "وصْفَ",
                            "وصل", "وضع", "وطن", "وعاء", "وفاء", "وفق", "وفيق", "وقت", "وقع", "وكال", "وكيل",
                            "ولاء", "ولف", "وهب", "وصفها", "وباء", "ونستون", "وضح", "وجب", "وقّع", "ولنغتون", "وحش",
                            "وفر", "وساطته", "ولادة", "ولي", "وفيات", "وزار", "وجّه", "وهماً", "وجَّه", "ويب", "وظيفة",
                            "وظائف", "وقائي"]

    sentence_splitter_exceptions = ["د.", "كي.", "في.", "آر.", "بى.", "جى.", "دى.", "جيه.", "ان.", "ال.", "سى.", "اس.",
                                    "اتش.", "اف."]
    token_split_exceptions = ["،", "*", "’", "‘", ",", "(", ")", "/", "[", "]", "|", "؛", "«", "»", "!", "-", "“", "”",
                              '"', "؟", ":", "…" , "\\", "\n"]
    sentence_splitters = ['.', '!', '؟', '\n']
    for token_split_exception in token_split_exceptions:
        text = text.replace(token_split_exception, " " + token_split_exception + " ")
    text = text.replace('  ', ' ')
    tokens = text.split()
    for i, token in enumerate(tokens):
        if token[-1] in sentence_splitters:
            is_exceptions = token in sentence_splitter_exceptions
            if not is_exceptions:
                tokens[i] = token[:-1] + ' ' + token[-1] + 'SENT_SPLITTER'
    tokens = ' '.join(tokens).split()
    for i, token in enumerate(tokens):
        if token.startswith('و'):
            is_exceptions = [token.startswith(exception) and len(token) <= len(exception) + 1 for exception in
                             tokenizer_exceptions]
            if True not in is_exceptions:
                tokens[i] = token[0] + ' ' + token[1:]
    text = (' '.join(tokens))
    text = text.replace(' وال', ' و ال')
    text = text.replace(' لل', ' ل ل')
    text = text.replace(' لإ', ' ل إ')
    text = text.replace(' بالأ', ' ب الأ')
    text = text.replace('وفقا ل', 'وفقا ل ')
    text = text.replace('نسبة ل', 'نسبة ل ')
    sentences = text.split('SENT_SPLITTER')
    return sentences

def Ner_stanza(text):
    doc = ner_stanza(text)
    return doc.ents

def qs_fill(lines,x=1):
    split=split_sentences(lines)
    # print(split)
    list_qs=[]
    list_ans=[]
    for sen in split:
      if len(sen)>8:
        # print(sen)
        list_entity=Ner_stanza(sen)
        if len(list_entity) !=0:
          if x==0:
            for entity in list_entity:
              # print(sen.replace(entity.text,"__"))
              sen=sen.replace(entity.text,"___")
          else :
            list_entity=random.choice(list_entity)
            sen=sen.replace(list_entity.text,"___")
            # list_ans.append(Ner_stanza(sen))
          list_ans.append(list_entity)
          # print(Ner_stanza(sen))
          list_qs.append(sen)

    return list_qs,list_ans

def clean_str(text):
    search = ["أ","إ","آ","ة","_","-","/",".","،"," و "," يا ",'"',"ـ","'","ى","\\",'\n', '\t','&quot;','?','؟','!']
    replace = ["ا","ا","ا","ه"," "," ","","",""," و"," يا","","","","ي","",' ', ' ',' ',' ? ',' ؟ ',' ! ']

    #remove tashkeel
    p_tashkeel = re.compile(r'[\u0617-\u061A\u064B-\u0652]')
    text = re.sub(p_tashkeel,"", text)

    p_longation = re.compile(r'(.)\1+')
    subst = r"\1\1"
    text = re.sub(p_longation, subst, text)

    text = text.replace('وو', 'و')
    text = text.replace('يي', 'ي')
    text = text.replace('اا', 'ا')

    for i in range(0, len(search)):
        text = text.replace(search[i], replace[i])

    text = text.strip()

    return text

def get_vec(n_model,dim, token):
    vec = np.zeros(dim)
    is_vec = False
    if token not in n_model.wv:
        _count = 0
        is_vec = True
        for w in token.split("_"):
            if w in n_model.wv:
                _count += 1
                vec += n_model.wv[w]
        if _count > 0:
            vec = vec / _count
    else:
        vec = n_model.wv[token]
    return vec

def calc_vec(pos_tokens, neg_tokens, n_model, dim):
    vec = np.zeros(dim)
    for p in pos_tokens:
        vec += get_vec(n_model,dim,p)
    for n in neg_tokens:
        vec -= get_vec(n_model,dim,n)

    return vec

def get_all_ngrams(text, nrange=3):
    text = re.sub(r'[\,\.\;\(\)\[\]\_\+\#\@\!\?\؟\^]', ' ', text)
    tokens = [token for token in text.split(" ") if token.strip() != ""]
    ngs = []
    for n in range(2,nrange+1):
        ngs += [ng for ng in ngrams(tokens, n)]
    return ["_".join(ng) for ng in ngs if len(ng)>0 ]

def get_ngrams(text, n=2):
    text = re.sub(r'[\,\.\;\(\)\[\]\_\+\#\@\!\?\؟\^]', ' ', text)
    tokens = [token for token in text.split(" ") if token.strip() != ""]
    ngs = [ng for ng in ngrams(tokens, n)]
    return ["_".join(ng) for ng in ngs if len(ng)>0 ]

def get_existed_tokens(tokens, n_model):
    return [tok for tok in tokens if tok in n_model.wv ]

def func_stemmer_1(text:str):
    stemmer = ISRIStemmer()
    stemmed_data = []
    stemmed_words = stemmer.stem(text)
    return stemmed_words

def dis_word_embed(word):
    token = clean_str(word)
    dis_list=[]
    dis_stem=[]
    if token in modell.wv:
        most_similar = modell.wv.most_similar( token, topn=10 )
        dis_stem.append(func_stemmer_1(token))

        for term, score in most_similar:
            term = clean_str(term)
            if term != token and len(term)>3 and len(dis_list)<3 and ((' ' in split_sentences(term)[0]) ==False) :
                # print(term, score)

                if func_stemmer_1(term) in dis_stem:
                  d=0

                else :
                  dis_stem.append(func_stemmer_1(term))
                  dis_list.append(term)
    return dis_list

def qs_multichoice(lines):
  qs_multi={'qs':[],'an':[],'all_an':[]}
  list_qs,list_ans=qs_fill(lines,x=1)
  for i,qs in enumerate(list_qs):

    all_answer=dis_word_embed(list_ans[i].text)

    if len(all_answer) ==3 and qs_multi['an'].count(list_ans[i].text) < 3 :

      qs_multi['an'].append(list_ans[i].text) # الجواب الصحيح
      all_answer.insert(0,list_ans[i].text) # الجواب الصحيح
      all_answer.sort()
      qs_multi['qs'].append(qs)
      qs_multi['all_an'].append(all_answer)
  return qs_multi

def qs_true_false(lines):
  qs_all=[]
  list_qs,list_ans=qs_fill(lines,x=1)
  for i,qs in enumerate(list_qs):
    qs_multi={'qs':[],'an':[],'rep':[],'all_an':["True","False"]}

    qs_multi['an'].append(list_ans[i].text) # الجواب الصحيح
    all_answer=dis_word_embed(list_ans[i].text)
    all_answer.insert(0,list_ans[i].text) # الجواب الصحيح

    answer=random.choice(all_answer)
    qs=qs.replace("___",answer)
    qs_multi['qs'].append(qs)

    if answer == list_ans[i].text:
      qs_multi['an'].append("True")
    else :
      qs_multi['an'].append("False")
      qs_multi['rep'].append(answer)


    qs_all.append(qs_multi)

  return qs_all

def get_question(context,answer):
  text="context: " +context + " " + "answer: " + answer + " </s>"
  text_encoding = tokenizer.encode_plus(
      text,return_tensors="pt"
  )
  model.eval()
  generated_ids =  model.generate(
    input_ids=text_encoding['input_ids'],
    attention_mask=text_encoding['attention_mask'],
    max_length=800,
    num_beams=5,
    num_return_sequences=1
  )
  return tokenizer.decode(generated_ids[0],skip_special_tokens=True,clean_up_tokenization_spaces=True).replace('question: ',' ')

def word_impoertant(text):
  list_qs={'qs':[],'context':[]}
  list_entity=Ner_stanza(text)
  for entity in list_entity:


    if (get_question(text,entity.text) in list_qs['qs'])==False :


      list_qs['qs'].append(get_question(text,entity.text))
      list_qs['context'].append(entity.text)

  return list_qs


def getQuestion(text):
    finalResult = {}
    lines = text
    finalData = []
    split=split_sentences(lines)
    QS=qs_multichoice(lines)
    QT=qs_true_false(lines)
    for i in range(QS["qs"].__len__()):
        op = []
        for j in range(QS["all_an"][i].__len__()):
            p = {
                "code" : str(j+1),
                "text" : QS["all_an"][i][j],
                "isCorrect" : bool(QS["an"][i] == QS["all_an"][i][j])
            }
            op.append(p)
        data = {
            "text" : QS["qs"][i],
            "option" : op
        }
        finalData.append(data)
    for i in range(QT.__len__()):
        op = []
        p1 = {
            "code" : str(1),
            "text" : "صح",
            "isCorrect" : QT[i]["an"].__contains__("True")
        }
        op.append(p1)
        p2 = {
            "code" : str(2),
            "text" : "خطأ",
            "isCorrect" : QT[i]["an"].__contains__("False")
        }
        op.append(p2)
        data = {
            "text" : QT[i]["qs"][0],
            "option" : op
        }
        finalData.append(data)
    listt=word_impoertant(lines[:3000])
    wiData = listt["qs"]
    list_fill_qs,list_fill_ans=qs_fill(lines,x=1)
    qsData = list_fill_qs
    finalResult = {
        "testQuestion" : finalData,
        "qs" : wiData,
        "wi" : qsData
    }
    return finalResult


