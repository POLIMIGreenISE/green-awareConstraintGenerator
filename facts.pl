serviceConnection(checkoutservice, currencyservice, 1.0036967316395136e-06, 0.0010036967316395136).
serviceConnection(checkoutservice, emailservice, 1.5336298900856789e-06, 0.0015336298900856789).
serviceConnection(checkoutservice, paymentservice, 4.222178494894573e-07, 0.0004222178494894573).
serviceConnection(checkoutservice, productcatalogservice, 6.026168169467995e-07, 0.0006026168169467995).
serviceConnection(checkoutservice, shippingservice, 1.4862172026675564e-06, 0.0014862172026675563).
serviceConnection(frontend, productcatalogservice, 3.193158733149987e-05, 0.031931587331499874).
serviceConnection(frontend, recommendationservice, 9.593180262514066e-06, 0.009593180262514066).
serviceConnection(frontend, shippingservice, 2.220275308095603e-06, 0.0022202753080956027).
serviceConnection(frontend, adservice, 4.701040297916905e-06, 0.004701040297916905).
serviceConnection(checkoutservice, cartservice, 7.824486654978678e-07, 0.0007824486654978678).
serviceConnection(frontend, cartservice, 1.0145732279670878e-05, 0.010145732279670878).
serviceConnection(frontend, checkoutservice, 1.0525099772343437e-06, 0.0010525099772343437).
serviceConnection(frontend, currencyservice, 2.126555646475965e-05, 0.021265556464759652).
serviceConnection(recommendationservice, productcatalogservice, 3.5704926921195376e-06, 0.0035704926921195377).
service(frontend, 2.610197924374597, 2610.1979243745973).
service(productcatalogservice, 1.1651327314335715, 1165.1327314335715).
service(currencyservice, 1.0373861440389631, 1037.386144038963).
service(recommendationservice, 0.7104935794186064, 710.4935794186064).
service(cartservice, 0.6440012042667275, 644.0012042667274).
service(adservice, 0.29613956743638964, 296.13956743638965).
service(checkoutservice, 0.1414632396938025, 141.4632396938025).
service(shippingservice, 0.1164683902427772, 116.4683902427772).
service(emailservice, 0.05966962691127832, 59.66962691127832).
service(paymentservice, 0.041158167184273474, 41.15816718427347).
node(france, 16).
node(spain, 88).
node(germany, 132).
node(greatbritain, 213).
node(italy, 335).
deployedTo(frontend,large,france).
deployedTo(productcatalogservice,large,greatbritain).
deployedTo(recommendationservice,large,germany).
deployedTo(checkoutservice,tiny,spain).
deployedTo(adservice,tiny,germany).
deployedTo(cartservice,tiny,greatbritain).
deployedTo(shippingservice,tiny,greatbritain).
deployedTo(currencyservice,tiny,greatbritain).
deployedTo(paymentservice,tiny,italy).
deployedTo(emailservice,tiny,italy).
highConsumptionService(frontend,large,spain,0.263).
highConsumptionService(frontend,large,greatbritain,0.636).
highConsumptionService(frontend,large,italy,1.000).
highConsumptionService(frontend,large,germany,0.394).
highConsumptionService(productcatalogservice,large,spain,0.117).
highConsumptionService(productcatalogservice,large,greatbritain,0.284).
highConsumptionService(productcatalogservice,large,italy,0.446).
highConsumptionService(productcatalogservice,large,germany,0.176).
