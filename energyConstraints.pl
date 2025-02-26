affinity(d(frontend,large),d(productcatalogservice,medium),0.376).
affinity(d(frontend,large),d(recommendationservice,large),0.085).
affinity(d(frontend,large),d(cartservice,small),0.09).
affinity(d(frontend,large),d(currencyservice,small),0.188).
avoid(d(frontend,large),node_b,0.445).
avoid(d(frontend,large),node_c,0.445).
avoid(d(productcatalogservice,medium),node_c,1.0).
