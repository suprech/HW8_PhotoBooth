import boto3
import os
import time
import subprocess
import sys

# hard coded credentials
access_key = "AKIAJZOZA5WTPBDERNZQ"
access_secret = "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" 
region = "us-east-1" 
queue_url = "https://sqs.us-east-1.amazonaws.com/762995444827/testQueue"


# client instance
client = boto3.client('sqs', aws_access_key_id = access_key, 
        aws_secret_access_key = access_secret, region_name = region)

# long polling for free tier usage. 
# polling waits for 20 sec for a message to arrive.
waittime = 20
client.set_queue_attributes(QueueUrl = queue_url, 
        Attributes = {'ReceiveMessageWaitTimeSeconds': str(waittime)})


# get the message from the AWS queue.
def pop_message(client, url):
    response = client.receive_message(QueueUrl = url, 
            MaxNumberOfMessages = 10)

    # last message posted becomes messages
    message = response['Messages'][0]['Body']
    receipt = response['Messages'][0]['ReceiptHandle']
    client.delete_message(QueueUrl = url, ReceiptHandle = receipt)
    return message


# return the message for gui.py
def message_handler():
    global client, queue_url

    return pop_message(client, queue_url)


if __name__ == "__main__":
    time_start = time.time()
    # wait for 60 sec
    # runs for only 1 minute. put it in while statement when use.
    while(time.time() - time_start < 60):
        print("Checking...")
        try:
            message = pop_message(client, queue_url)
            print(message)
            # 'message' is used to split cases.
            # shutter >> take a picture
            # sepia >> apply sepia
            # gray >> apply grayscale
            # undo >> undo the filter applying
            # print >> send the photo to the printer
            # upload >> upload the photo to the webserver
            if(message == 'Run1'):
                #os.system("")
                #slave.function()
                subprocess.Popen([sys.executable, 'slave.py'], shell=True)

        except:
            pass
