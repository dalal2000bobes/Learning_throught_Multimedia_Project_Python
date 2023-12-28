# importing libraries
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import nltk
import pickle
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer, sent_tokenize

def getSummaryExtractive(text):
    # Tokenizing the text

    stopWords = set(stopwords.words("arabic"))
    words = TweetTokenizer().tokenize(text)

    # Creating a frequency table to keep the
    # score of each word

    freqTable = dict()
    for word in words:
        word = word.lower()
        if word in stopWords:
            continue
        if word in freqTable:
            freqTable[word] += 1
        else:
            freqTable[word] = 1

    # Creating a dictionary to keep the score
    # of each sentence

    sentences = sent_tokenize(text)
    sentenceValue = dict()

    for sentence in sentences:
        for word, freq in freqTable.items():
            if word in sentence.lower():
                if sentence in sentenceValue:
                    sentenceValue[sentence] += freq
                else:
                    sentenceValue[sentence] = freq
    sumValues = 0
    for sentence in sentenceValue:
        sumValues += sentenceValue[sentence]

    # Average value of a sentence from the original text

    average = int(sumValues / len(sentenceValue))

    # Storing sentences into our summary.

    summary = ''
    for sentence in sentences:
        if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.2 * average)):
            summary += " " + sentence

    print("Done ...")
    return summary

model_name = "csebuetnlp/mT5_multilingual_XLSum"
abstractive_Tokenizer = AutoTokenizer.from_pretrained(model_name)
abstractive_Model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

def abstractiveModelSummarizer(text):
  input_ids = abstractive_Tokenizer(
      [(text)],
      return_tensors="pt",
      padding="max_length",
      truncation=True,
      max_length=2000
  )["input_ids"]

  output_ids = abstractive_Model.generate(
      input_ids=input_ids,
      max_length=600,
      no_repeat_ngram_size=8,
      num_beams=4
  )[0]

  summary = abstractive_Tokenizer.decode(
      output_ids,
      skip_special_tokens=True,
      clean_up_tokenization_spaces=False
  )
  return summary

# def getSummaryAbstractive(text):
#     abstractiveModel = pickle.load(open('Files/Models/abstractiveModel.pkl', 'rb'))
#     the_result_abstractive = abstractiveModel(text)
#     print(the_result_abstractive)
#     return the_result_abstractive