affinity(d(frontend,large),d(productcatalogservice,medium),0.38).
affinity(d(frontend,large),d(currencyservice,small),0.253).
avoid(d(productcatalogservice,medium),node_b,0.931).
avoid(d(currencyservice,small),node_b,1.0).
