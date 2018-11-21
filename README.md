<h3><a href="https://cloud.google.com/dataflow/docs/">Google DataFlow</a></h3>
Deploy batch and streaming data processing pipelines, based on <a href="https://beam.apache.org/">Apache Beam</a>. Pipelines are created using the Apache Beam SDK and ran on the managed, Cloud Dataflow service.
<br>
<br><b>Concepts:</b>
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Both batch and Real-time Processing
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Built on Apache Beam
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;No-ops, serverless
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Automatic Tuning - Auto-scales to multiple machines (max_num_workers) 
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Dynamic Work Rebalancing (re-partition work based on runtime conditions)
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Parallelization and Distribution - Automatically partitions data and distributes worker code
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;DataflowRunner (cloud deployment) vs. DirectRunner (local)
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Max of <b>25 concurrent Dataflow jobs per GCP project</b>. (< 10MB, based on JSON repr of pipeline)
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Dataflow allows a max of 1000 Compute Engine instances per job (4000 cores / job)
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;<b>Components</b>
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&ndash;&nbsp;<b>Element:</b> data (single row)
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&ndash;&nbsp;<b>PCollection:</b> Potentially distributed, multi-element data set
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&ndash;&nbsp;<b>Transforms:</b> Operations (math, loops, conditionals) in pipeline
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&ndash;&nbsp;<b>ParDo:</b> Special type of transform (Extract or Filter out one column of data)
<br><b>Guidelines: When structuring ParDo transforms and creating DoFn</b>
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&ndash;&nbsp;Dataflow guarantees that every element in your input PCollection is processed by a DoFn instance exactly once
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&ndash;&nbsp;Dataflow does not guarantee how many times a DoFn will be invoked.
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&ndash;&nbsp;Dataflow does not guarantee exactly how the distributed elements are grouped
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&ndash;&nbsp;Dataflow does not guarantee exact number of DoFn instances created over the course of a pipeline
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&ndash;&nbsp;Dataflow is fault-tolerant, and may retry your code multiple times
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&ndash;&nbsp;Dataflow may create backup copies of your code
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&ndash;&nbsp;Dataflow serializes element processing per DoFn instance. Code doesnt need to be thread-safe
<br>
<br><b><a href="https://beam.apache.org/documentation/programming-guide/#windowing">Windowing</a></b>
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Fixed Time Windows
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Sliding Time Windows
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Per-Session Windows
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Single Global Window
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Calendar-based Windows (not supported by the Beam SDK for Python)
<br>
<br><b>Handle Out-of-Order or Late Data</b>
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Resolve with windows, watermarks, or triggers
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Windows (logically divides element groups by time span)
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Watermarks (timestamp - Event Time or Processing Time or PubSub Source Generated)
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Triggers (Determines when results within window are emitted). 
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&ndash;&nbsp;Event time triggers (default trigger) - operate on event time as indicated by timestamp
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&ndash;&nbsp;Processing time triggers
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&ndash;&nbsp;Data-driven triggers - operate by examining data as it arrives in each window
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&ndash;&nbsp;Composite triggers
<br>
<br><b>Fusion Optimization</b>
<br>Once the JSON form of your pipeline's execution graph has been validated, the Cloud Dataflow service may modify the graph to perform optimizations. Fusing steps prevents the Cloud Dataflow service from needing to materialize every intermediate PCollection in your pipeline, which can be costly in terms of memory and processing overhead.
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
<br><b>IAM</b>
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Project-level ONLY (all or nothing for dataflow pipelines within a project)
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Roles:
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&ndash;&nbsp;roles/dataflow.admin
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&ndash;&nbsp;roles/dataflow.developer
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&ndash;&nbsp;roles/dataflow.viewer
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&ndash;&nbsp;roles/dataflow.worker (for controller service accounts only)
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Dataflow uses two service accounts to manage security and permissions:
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&ndash;&nbsp;Dataflow service account (create and manage job)
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&ndash;&nbsp;Controller service account (worker instances)
<br>
