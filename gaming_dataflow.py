

################################################################################################################
#
#   Google Cloud Dataflow
#
#   References:
#   https://cloud.google.com/dataflow/docs/
#
#   Usage:
'''
python gaming_dataflow.py \
    --gcp_project gaming-demos \
    --region us-central1 \
    --job_name 'gamelogs' \
    --gcp_staging_location "gs://gaming-dataflow/staging" \
    --gcp_tmp_location "gs://gaming-dataflow/tmp" \
    --batch_size 10 \
    --input_topic projects/gaming-demos/topics/game-logs \
    --bq_dataset_name streaming \
    --bq_table_name game_logs \
    --runner DirectRunner
    --runner DataflowRunner &
'''
#
################################################################################################################


from __future__ import absolute_import
import logging
import argparse
import json
import apache_beam as beam
from apache_beam import window
from apache_beam.transforms import trigger
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import StandardOptions
from apache_beam.options.pipeline_options import SetupOptions
from apache_beam.io import ReadFromText
from apache_beam.io import WriteToText
from past.builtins import unicode

################################################################################################################
#
#   Variables
#
################################################################################################################

bq_schema = {'fields': [
    {'name': 'uid',         'type': 'STRING', 'mode': 'NULLABLE'},
    {'name': 'game_id',     'type': 'STRING', 'mode': 'NULLABLE'},
    {'name': 'game_server', 'type': 'STRING',  'mode': 'NULLABLE'},
    {'name': 'game_type',   'type': 'STRING',  'mode': 'NULLABLE'},
    {'name': 'game_map',    'type': 'STRING',  'mode': 'NULLABLE'},
    {'name': 'event_datetime',   'type': 'STRING',  'mode': 'NULLABLE'},
    {'name': 'player',      'type': 'STRING',  'mode': 'NULLABLE'},
    {'name': 'killed',      'type': 'STRING',  'mode': 'NULLABLE'},
    {'name': 'weapon',      'type': 'STRING',  'mode': 'NULLABLE'},
    {'name': 'x_cord',      'type': 'INT64',  'mode': 'NULLABLE'},
    {'name': 'y_cord',      'type': 'INT64',  'mode': 'NULLABLE'}
]}

################################################################################################################
#
#   Functions
#
################################################################################################################

def parse_pubsub(line):
    return json.loads(line)


def extract_map_type(event):
    return event['game_map']

def sum_by_group(GroupByKey_tuple):
      (word, list_of_ones) = GroupByKey_tuple
      return {"word":word, "count":sum(list_of_ones)}

def run(argv=None):
    """Build and run the pipeline."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--gcp_project',          required=True,  default='',                   help='GCP Project ID')
    parser.add_argument('--region',               required=True,  default='',                   help='GCP Project ID')
    parser.add_argument('--job_name',             required=True,  default='',                   help='Dataflow Job Name')
    parser.add_argument('--gcp_staging_location', required=True,  default='gs://xxxxx/staging', help='Dataflow Staging GCS location')
    parser.add_argument('--gcp_tmp_location',     required=True,  default='gs://xxxxx/tmp',     help='Dataflow tmp GCS location')
    parser.add_argument('--batch_size',           required=True,  default=10,                   help='Dataflow Batch Size')
    parser.add_argument('--input_topic',          required=True,  default='',                   help='Input PubSub Topic: projects/<project_id>/topics/<topic_name>')
    parser.add_argument('--bq_dataset_name',      required=True,  default='',                   help='Output BigQuery Dataset')
    parser.add_argument('--bq_table_name',        required=True,  default='',                   help='Output BigQuery Table')
    parser.add_argument('--runner',               required=True,  default='DirectRunner',       help='Dataflow Runner - DataflowRunner or DirectRunner (local)')
    
    known_args, pipeline_args = parser.parse_known_args(argv)
    
    pipeline_args.extend([
          '--runner={}'.format(known_args.runner),                          # DataflowRunner or DirectRunner (local)
          '--project={}'.format(known_args.gcp_project),
          '--staging_location={}'.format(known_args.gcp_staging_location),  # Google Cloud Storage gs:// path
          '--temp_location={}'.format(known_args.gcp_tmp_location),         # Google Cloud Storage gs:// path
          '--job_name=' + str(known_args.job_name),
      ])
    
    pipeline_options = PipelineOptions(pipeline_args)
    pipeline_options.view_as(SetupOptions).save_main_session = True
    pipeline_options.view_as(StandardOptions).streaming = True
    
    ###################################################################
    #   DataFlow Pipeline
    ###################################################################
    
    with beam.Pipeline(options=pipeline_options) as p:
        
        logging.info('Ready to process events from PubSub topic: {}'.format(known_args.input_topic))
        
        # Read the pubsub topic into a PCollection.
        events = ( 
                 p  | beam.io.ReadFromPubSub(known_args.input_topic) 
        )
        
        # Parse events
        parsed = (
            events  | beam.Map(parse_pubsub)
        )
        
        # Tranform events
        transformed = (
            parsed  | beam.Map(extract_map_type)
                    | beam.Map(lambda x: (x, 1))
                    | beam.WindowInto(window.SlidingWindows(30, 5)) # Window is 30 seconds in length, and a new window begins every five seconds
                    | beam.GroupByKey()
                    | beam.Map(sum_by_group)
        )
        
        # Print results to console (for testing/debugging)
        transformed | 'Print aggregated game logs' >> beam.Map(print)
        
        # Sink/Persist to BigQuery
        parsed | 'Write to bq' >> beam.io.gcp.bigquery.WriteToBigQuery(
                        table=known_args.bq_table_name,
                        dataset=known_args.bq_dataset_name,
                        project=known_args.gcp_project,
                        schema=bq_schema,
                        batch_size=int(known_args.batch_size)
                        )
        
        # Sink data to PubSub
        #output | beam.io.WriteToPubSub(known_args.output_topic)


################################################################################################################
#
#   Main
#
################################################################################################################

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    run()



'''
python ./stream_game_events.py --project_id gaming-demos --bq_dataset_id streaming --bq_table_id game_logs --pubsub_topic game-logs --sink pubsub --number_of_records 10 --delay 2
'''



#ZEND
