# Message Dumper tool

This samples provides a simple utility for writing the contents of a
CloudEvents message (data and attributes) to both a log file and an
in-memory list. Because it can be run as either a [Kubernetes
Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
or a [Knative Service](https://github.com/knative/docs/tree/master/serving),
it provides an interesting opportunity to compare the two approaches.

It also provides a handy utility for debugging flows when working with
CloudEvents, and showcases a build template for converting simple python
code into a container capable of processing CloudEvents messages.

## Prerequisites

Install [Knative Build](https://github.com/knative/docs/tree/master/build)
and [Knative Serving](https://github.com/knative/docs/tree/master/serving).

Install the following build template:

```shell
kubectl apply -f https://github.com/evankanderson/pyfun/tree/master/packaging/build-template.yaml
```

## Deployment

To deploy using Serving, use the `service.yaml` file, which will build the
container and then deploy it.

## Sending Events

TODO
