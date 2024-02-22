package main

import (
    "bytes"
    "context"
    "fmt"
    "log"
    "github.com/elastic/go-elasticsearch/v8"
  )
  
  // ...
  
  cfg := elasticsearch.Config{
    Addresses: []string{
      "https://elastic.openknowit.com",
    },
    APIKey: "",
  }
  
  es, err := elasticsearch.NewClient(cfg)
  if err != nil {
    log.Fatalf("Error creating the client: %s", err)
  }
