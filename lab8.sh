#!/bin/bash

mvn clean -Dtest=TestJpa test -pl docs-core
mvn jacoco:report
mvn site
mvn site:stage
