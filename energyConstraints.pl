affinity(d(frontend,large),d(productcatalogservice,medium),0.168).
affinity(d(frontend,large),d(recommendationservice,large),0.168).
affinity(d(frontend,large),d(cartservice,small),0.168).
affinity(d(frontend,large),d(currencyservice,small),0.168).
avoid(d(frontend,large),node_b,0.41).
avoid(d(frontend,large),node_c,0.41).
avoid(d(productcatalogservice,medium),node_c,1.0).
