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
<br>
<br><b>Components</b>
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;<b>Element:</b> data (single row)
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;<b>PCollection:</b> Potentially distributed, multi-element data set
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;<b>Transforms:</b> Operations (math, loops, conditionals) in pipeline
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;<b>ParDo:</b> Special type of transform (Extract or Filter out one column of data)
<br>
<br><b><a href="https://beam.apache.org/documentation/programming-guide/#windowing">Windowing</a></b>
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Fixed Time Windows
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Sliding Time Windows (i.e. 1 minute window duration and 30 window period)
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Per-Session Windows
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&ndash;&nbsp;Defines windows that contain elements within a certain gap duration of another element
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&ndash;&nbsp;Session windowing applies on a per-key basis
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&ndash;&nbsp;Useful for data irregularly distributed with respect to time
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&ndash;&nbsp;If data arrives after the minimum specified gap duration, this initiates start of new window
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Single Global Window
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Calendar-based Windows (not supported by the Beam SDK for Python)
<br>
<br><b><a href="https://beam.apache.org/documentation/programming-guide/#triggers">Triggers</a></b> (Determines when results within window are emitted)
<br>Triggers determine when to emit the aggregated results of each window. Emits data after a certain amount of time elapses, or after a certain number of elements arrive. Triggers allow processing of late data by triggering after the event time watermark passes the end of the window. Beam provides a number of pre-built triggers:
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Event time triggers (default trigger) - Operate on event time as indicated by timestamp
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Processing Time Triggers - Operates when the data element is processed
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Data-driven triggers - Operate by examining data as it arrives in each window
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Composite triggers
<br>
<br><b>Handle Out-of-Order or Late Data</b>
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Resolve with windows, watermarks, or triggers
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Windows (logically divides element groups by time span)
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Watermarks (timestamp - Event Time or Processing Time or PubSub Source Generated)
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Triggers (Determines when results within window are emitted). 
<br>
<br><b>Side Inputs</b>
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Useful when you need to reference external data within a Transform (i.e. list of tax rates, external source, etc.)
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Side inputs are useful if your ParDo needs to inject additional data when processing each element in PCollection
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Additional inputs to a ParDo transform
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Input that your DoFn can access each time it processes an element in the input PCollection
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Can also turn PCollection into a VIEW, which is used in another PCollection Transform.
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;A VIEW can be either a LIST (PCollection of object) or MAP (PCollection of key:value pairs)
<br>
<br><b>Guidelines: When structuring ParDo transforms and creating DoFn</b>
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Dataflow guarantees that every element in your input PCollection is processed by a DoFn instance exactly once
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Dataflow does not guarantee how many times a DoFn will be invoked.
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Dataflow does not guarantee exactly how the distributed elements are grouped
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Dataflow does not guarantee exact number of DoFn instances created over the course of a pipeline
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Dataflow is fault-tolerant, and may retry your code multiple times
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Dataflow may create backup copies of your code
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Dataflow serializes element processing per DoFn instance. Code doesnt need to be thread-safe
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
