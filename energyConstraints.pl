affinity(d(frontend,large),d(productcatalogservice,medium),0.0).
affinity(d(frontend,large),d(recommendationservice,large),0.0).
affinity(d(frontend,large),d(cartservice,small),0.0).
affinity(d(frontend,large),d(currencyservice,small),0.0).
avoid(d(productcatalogservice,medium),node_c,0.799).
avoid(d(currencyservice,small),node_c,1.0).
