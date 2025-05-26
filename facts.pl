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
highConsumptionService(frontend,large,greatbritain,0.636).
highConsumptionService(frontend,large,italy,1.000).
highConsumptionService(productcatalogservice,large,italy,0.446).
