## Deploying a dummy tensorflow model to reproduce the recursion error

1. Create a bucket, say: `bucket11`
2. Upload the sample json object `data.json`  to the bucket
3. rename the bucket name in `code1/inference.py` to the name of the bucket you created. The specific line in the script is: 
```
...
json_object = s3_client.get_object(Bucket="bucket11", Key=key)
...
```
4. Start a sagemaker notebook instance. For this test, I used an `ml.t3.medium` instance
5. Launch Jupyterlab from the instance, upload the notebook `test.ipnb` to the directory. Next, create a folder named `code1` in the directory and upload the files in `code1` of this repo to the newly created folder. Nest, upload the 
   Alternatively, launch jupyterlab, click on the Git tab, from the dropdown select `Clone a Repository`. Enter the URI: `https://github.com/MustaphaU/rerror.git` and hit `Clone`.
6. Run all the codes in the noteboook `test.ipynb`.
7. The last cell should throw the error:
```
ModelError: An error occurred (ModelError) when calling the InvokeEndpoint operation: Received server error (500) from primary with message "{"error": "cannot unpack non-iterable NoneType object"}". See https://us-west-2.console.aws.amazon.com/cloudwatch/home?region=us-west-2#logEventViewer:group=/aws/sagemaker/Endpoints/tensorflow-inference-....... in account [account_id] for more information.
```

8. Click the link to the cloudwatch log in the above error message. In the logs you will find:
   ```
   maximum recursion depth exceeded while calling a Python object
   ```


