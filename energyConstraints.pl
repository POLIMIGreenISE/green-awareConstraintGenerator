affinity(d(frontend,large),d(productcatalogservice,medium),0.315).
affinity(d(frontend,large),d(recommendationservice,large),0.071).
affinity(d(frontend,large),d(cartservice,small),0.075).
affinity(d(frontend,large),d(currencyservice,small),0.21).
avoid(d(productcatalogservice,medium),node_b,0.881).
avoid(d(currencyservice,small),node_a,1.0).
avoid(d(currencyservice,small),node_b,1.0).
avoid(d(currencyservice,small),node_c,1.0).
