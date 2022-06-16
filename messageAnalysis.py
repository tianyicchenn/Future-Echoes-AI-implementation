import pandas as pd
import openai
import json


def retract_credentials():
    with open("credentials.json", "r") as read_file:
        data = json.load(read_file)
        openai.organization = data["organization"]
        openai.api_key = data["api_key"]
    return


#TODO:add content filter


def generate_keywords(userinput):
    makePrompt = "extract keywords from this text:\n\n" + userinput + "\n"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=makePrompt,
        temperature=0.3,
        max_tokens=60,
        top_p=1.0,
        frequency_penalty=0.8,
        presence_penalty=0.0
    )
    return response['choices'][0]['text'].strip('\n').strip('.')


def sentiment_analysis(userinput):
    makePrompt = "Decide whether a Tweet's sentiment is positive, neutral, or negative.\n\nTweet:" + userinput + "\n"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=makePrompt,
        temperature=0,
        max_tokens=60,
        top_p=1,
        frequency_penalty=0.5,
        presence_penalty=0
    )
    output = response["choices"][0]["text"].strip('\n')
    if 'positive' in output:
        return 'positive'
    elif 'neutral' in output:
        return 'neutral'
    elif 'negative' in output:
        return 'negative'
    else:
        return 'error'

def generate_id(topic):
    answers = pd.read_csv('data_test.csv', sep=';')
    num = answers['topic'].value_counts()[topic] + 1
    id = 't' + str(topic) + 'a' + str(num)
    return id


def update_data(topic, id, text, keywords, sentiment):
    newEntry = pd.DataFrame({'topic': [topic],
                             'id': [id],
                             'text': [text],
                             'keywords': [keywords],
                             'sentiment': [sentiment]})
    oldFile = pd.read_csv('data_test.csv', sep=';')
    newFile = pd.concat([oldFile, newEntry], ignore_index=True)
    print(newFile)
    newFile.to_csv('data_test.csv', sep=';', index=False)


def update_visualisation():
    data = pd.read_csv('data_test.csv', sep=';')
    with open('visualisation/keywords.txt', 'w') as f:
        for strings in data['keywords'].values:
            f.write(strings + '\n')
        f.close()

    with open('visualisation/sentiment.txt', 'w') as f:
        for strings in data['sentiment'].values:
            f.write(strings + '\n')
        f.close()



if __name__ == '__main__':
    retract_credentials()
    topic = 3
    userInput = "technology"
    keywords = generate_keywords(userInput)
    sentiment = sentiment_analysis(userInput)
    print(keywords)
    print(sentiment)

    id = generate_id(topic)

    update_data(topic, id, userInput, keywords, sentiment)
    update_visualisation()