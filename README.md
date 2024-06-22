## Deploying a Dummy TensorFlow Model to Reproduce the Recursion Error

Follow these steps to set up and reproduce the [maximum recursion depth exceeded](https://github.com/boto/boto3/issues/4061)  error when trying to read s3 objects via an inference script:

1. **Create an S3 Bucket:**
   - Create a bucket, for example, named `bucket11`.

2. **Upload Sample Data:**
   - Upload the sample JSON object `data.json` to the created bucket.

3. **Update the Bucket Name in the Script:**
   - Modify the `code1/inference.py` script to use the name of the bucket you created. Change the bucket name in the `get_json_from_s3` function:
     ```python
     ...
     json_object = s3_client.get_object(Bucket="bucket11", Key=key)
     ```

4. **Start a SageMaker Notebook Instance:**
   - Launch an `ml.t3.medium` SageMaker notebook instance.

5. **Set Up JupyterLab:**
   - Launch JupyterLab from the SageMaker instance.
   - Upload the notebook `test.ipynb` to the JupyterLab directory.
   - Create a folder named `code1` in the directory and upload all files from the `code1` folder of this repository into it.

6. **Clone the Repository (Alternative Setup to 5):**
   - Alternatively, you can clone the repository directly into JupyterLab:
     - Open the Git tab, select `Clone a Repository` from the dropdown, enter the URI: `https://github.com/MustaphaU/rerror.git`, and hit `Clone`.

7. **Run the Notebook:**
   - Execute all the code cells in the `test.ipynb` notebook.

8. **Identify the Error:**
   - The last cell should generate the following error:
     ```
     ModelError: An error occurred (ModelError) when calling the InvokeEndpoint operation: Received server error (500) from primary with message "{"error": "cannot unpack non-iterable NoneType object"}".....................................
     ```
     This error is due to the `get_json_from_s3` function returning None because of the recursion error during the setup of the S3 client. See the linked CloudWatch logs for more details on the recursion error.

9. **Review CloudWatch Logs:**
   - Click the link provided in the error message to view the CloudWatch logs. In the logs, you will find:
     ```
     maximum recursion depth exceeded while calling a Python object
     ```
