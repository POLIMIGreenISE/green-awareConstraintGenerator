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
service(frontend, 1.9816222897140123, 1981.6222897140124).
service(productcatalogservice, 0.8845509260135269, 884.5509260135269).
service(currencyservice, 0.7875676732677762, 787.5676732677762).
service(recommendationservice, 0.5393958444787067, 539.3958444787067).
service(cartservice, 0.48891585157603834, 488.91585157603834).
service(adservice, 0.22482462430078812, 224.82462430078812).
service(checkoutservice, 0.10739672510449999, 107.39672510449999).
service(shippingservice, 0.0884210181906018, 88.4210181906018).
service(emailservice, 0.04530026692693778, 45.30026692693778).
service(paymentservice, 0.031246650200165902, 31.246650200165902).
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
highConsumptionConnection(frontend,large,productcatalogservice,medium,0.233).
highConsumptionConnection(frontend,large,currencyservice,small,0.233).
highConsumptionConnection(frontend,large,cartservice,small,0.233).
highConsumptionConnection(frontend,large,recommendationservice,large,0.233).
highConsumptionService(frontend,large,node_b,0.307).
highConsumptionService(frontend,large,node_c,0.307).
highConsumptionService(productcatalogservice,medium,node_c,1.000).
