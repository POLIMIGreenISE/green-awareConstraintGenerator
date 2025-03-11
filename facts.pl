serviceConnection(checkoutservice, currencyservice, 1.5000160591477063, 1500.0160591477063).
serviceConnection(checkoutservice, emailservice, 1.5000245380782413, 1500.0245380782412).
serviceConnection(checkoutservice, paymentservice, 1.5000067554855918, 1500.0067554855918).
serviceConnection(checkoutservice, productcatalogservice, 1.5000096418690712, 1500.0096418690712).
serviceConnection(checkoutservice, shippingservice, 1.5000237794752427, 1500.0237794752427).
serviceConnection(frontend, productcatalogservice, 1.500510905397304, 1500.510905397304).
serviceConnection(frontend, recommendationservice, 1.5001534908842002, 1500.1534908842002).
serviceConnection(frontend, shippingservice, 1.5000355244049295, 1500.0355244049294).
serviceConnection(frontend, adservice, 1.5000752166447666, 1500.0752166447667).
serviceConnection(checkoutservice, cartservice, 1.500012519178648, 1500.012519178648).
serviceConnection(frontend, cartservice, 1.5001623317164747, 1500.1623317164747).
serviceConnection(frontend, checkoutservice, 1.5000168401596357, 1500.0168401596356).
serviceConnection(frontend, currencyservice, 1.500340248903436, 1500.340248903436).
serviceConnection(recommendationservice, productcatalogservice, 1.5000571278830739, 1500.057127883074).
service(frontend, 2.746827088943369, 2746.827088943369).
service(productcatalogservice, 1.2261208696206947, 1226.1208696206947).
service(currencyservice, 1.091687467655724, 1091.687467655724).
service(recommendationservice, 0.7476839178526924, 747.6839178526924).
service(cartservice, 0.6777110412482766, 677.7110412482766).
service(adservice, 0.311640806371857, 311.64080637185697).
service(checkoutservice, 0.14886804378013904, 148.86804378013903).
service(shippingservice, 0.12256485469435824, 122.56485469435823).
service(emailservice, 0.06279299590904182, 62.79299590904182).
service(paymentservice, 0.043312565494476894, 43.31256549447689).
node(node_a, 27).
node(node_b, 35).
node(node_c, 25).
deployedTo(frontend,large,node_a).
deployedTo(productcatalogservice,medium,node_b).
deployedTo(recommendationservice,large,node_b).
deployedTo(checkoutservice,large,node_b).
deployedTo(adservice,small,node_c).
deployedTo(cartservice,small,node_c).
deployedTo(shippingservice,small,node_c).
deployedTo(currencyservice,small,node_c).
deployedTo(paymentservice,small,node_c).
deployedTo(emailservice,small,node_c).
highConsumptionService(frontend,large,node_b,0.327).
highConsumptionService(frontend,large,node_c,0.327).
highConsumptionService(productcatalogservice,medium,node_c,0.799).
highConsumptionService(currencyservice,small,node_c,1.000).
