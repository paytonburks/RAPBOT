import pandas as pd
import tensorflow as tf
from transformers import AutoTokenizer, AutoModelForMaskedLM,\
                        TextDataset, DataCollatorForLanguageModeling,\
                        Trainer, TrainingArguments, AutoModelWithLMHead
from sklearn.model_selection import train_test_split


def load_dataset(train_path,test_path,tokenizer):
    train_dataset = TextDataset(
          tokenizer=tokenizer,
          file_path=train_path,
          block_size=128)

    test_dataset = TextDataset(
          tokenizer=tokenizer,
          file_path=test_path,
          block_size=128)

    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer, mlm=False,
    )
    return train_dataset, test_dataset, data_collator



def main():
    df = pd.read_csv('./tweets/thugtweets.csv')
    tweets = df['tweet']
    tweet_list = tweets.values.tolist()

    # prep data for fine-tuning
    train, test = train_test_split(tweets, test_size=.2, shuffle=True)
    train.to_csv(r'thug_train.txt')
    test.to_csv(r'thug_test.txt')

    # model time
    tokenizer = AutoTokenizer.from_pretrained("vinai/bertweet-base")

    train_path = 'thug_train.txt'
    test_path = 'thug_test.txt'

    train_dataset, test_dataset, data_collator = load_dataset(train_path, test_path, tokenizer)

    model = AutoModelForMaskedLM.from_pretrained("vinai/bertweet-base")

    # train up
    training_args = TrainingArguments(
        output_dir="./thug-bertweet-output",
        overwrite_output_dir=True,
        num_train_epochs=3,
        per_device_train_batch_size=32,
        per_device_eval_batch_size=64,
        eval_steps=400,
        save_steps=800,
        warmup_steps=500
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=train_dataset,
        eval_dataset=test_dataset
    )

    trainer.train()

    trainer.save_model()
    
    # with open('thugtext.txt', 'w') as f:
    #     f.write(text)


if __name__ == "__main__":
    main()
    