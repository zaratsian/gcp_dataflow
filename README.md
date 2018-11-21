<h3><a href="https://cloud.google.com/dataflow/docs/">Google DataFlow</a></h3>
Deploy your batch and streaming data processing pipelines, based on <a href="https://beam.apache.org/">Apache Beam</a>. Create your pipelines using the Apache Beam SDK, and run them on the Cloud Dataflow service.
<br>
<br><b>Concepts:</b>
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Batch and Real-time Processing
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Built on Apache Beam
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;No-ops, serverless
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Auto-scaling
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;<b>Components</b>
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;<b>Element:</b> data (single row)
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;<b><b>PCollection:</b> Potentially distributed, multi-element data set
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;<b>Transforms:</b> Operations (math, loops, conditionals) in pipeline
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;<b>ParDo:</b> Special type of transform (Extract or Filter out one column of data)
<br>
<br><b>Regional Endpoints (defaults to us-central1)</b>
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Stores and handles metadata about your Cloud Dataflow job
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Deploys and controls your Cloud Dataflow workers.
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;If you do not specify a regional endpoint, Dataflow uses us-central1 as the default region
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Why specify a regional endpoint?
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&ndash;&nbsp;Security and compliance (constrain Dataflow job to a specific geo region)
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&ndash;&nbsp;Data locality (minimize network latency and network transport costs)
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&ndash;&nbsp;Resilience and geographic separation
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&ndash;&nbsp;Auto Zone placement (By default, automatically selects best zone within a region)
<br>
<br><b>Pipeline Shutdown</b>
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Drain - Finish processing buffered jobs before shutting down
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Cancel - Full stop, cancels existing buffered jobs
<br>
<br><Handle Out-of-Order or Late Data</b>
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Resolve with windows, watermarks, or triggers
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Windows (logically divides element groups by time span)
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Watermarks (timestamp - Event Time or Processing Time or PubSub Source Generated)
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Triggers (Determines when results within window are emitted / submitted)
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;
<br>
<br><b>IAM</b>
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Roles:
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&ndash;&nbsp;roles/dataflow.admin
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&ndash;&nbsp;roles/dataflow.developer
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&ndash;&nbsp;roles/dataflow.viewer
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&ndash;&nbsp;roles/dataflow.worker (for controller service accounts only)
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Dataflow uses two service accounts to manage security and permissions:
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&ndash;&nbsp;Dataflow service account (create and manage job)
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&ndash;&nbsp;Controller service account (worker instances)
<br>
