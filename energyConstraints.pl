affinity(d(frontend,large),d(productcatalogservice,medium),0.134).
affinity(d(frontend,large),d(recommendationservice,large),0.03).
affinity(d(frontend,large),d(cartservice,small),0.032).
affinity(d(frontend,large),d(currencyservice,small),0.067).
avoid(d(frontend,large),node_b,0.158).
avoid(d(frontend,large),node_c,0.158).
avoid(d(productcatalogservice,medium),node_c,0.355).
avoid(d(currencyservice,small),node_c,0.397).
