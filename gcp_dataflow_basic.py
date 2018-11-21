

########################################################################################
#
#   Google Dataflow - Quickstart
#
#   https://cloud.google.com/dataflow/docs/quickstarts/quickstart-python
#
########################################################################################


########################################################################################
#   ENV Variables
########################################################################################


project_id=zproject201807
bucket_name=zdataflow_bucket


########################################################################################
#   Prerequisites
########################################################################################


sudo apt-get install git
sudo pip install virtualenv
pip install virtualenv


########################################################################################
#   Create Google Cloud Storage Bucket
########################################################################################


gsutil mb gs://$bucket_name


########################################################################################
#   Enter Python VirtualEnv
########################################################################################


virtualenv -p /usr/bin/python2.7 ~/dataflow_virtualenv
sudo chmod 775 ~/dataflow_virtualenv/bin/activate
source ~/dataflow_virtualenv/bin/activate

# Install python dependencies
echo "[ INFO ] Installing python dependencies..."
pip install apache-beam[gcp]


########################################################################################
#   Clone Git Repo
########################################################################################


git clone https://github.com/apache/beam.git


########################################################################################
#   Execute Dataflow Pipeline (Locally using DirectRunner)
########################################################################################


python beam/sdks/python/apache_beam/examples/wordcount.py --output /tmp/dataflow_output
head -n 20 /tmp/dataflow_output*


########################################################################################
#   Execute Dataflow Pipeline (Cloud deployed using DataflowRunner)
########################################################################################


python beam/sdks/python/apache_beam/examples/wordcount.py   \
    --input gs://dataflow-samples/shakespeare/kinglear.txt  \
    --output gs://$bucket_name/counts                       \
    --runner DataflowRunner                                 \
    --project $project_id                                   \
    --temp_location gs://$bucket_name/tmp/



#ZEND
