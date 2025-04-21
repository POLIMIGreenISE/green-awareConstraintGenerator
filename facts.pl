serviceConnection(checkoutservice, currencyservice, 3.4794820030169803e-09, 3.4794820030169804e-06).
serviceConnection(checkoutservice, emailservice, 5.316583618963687e-09, 5.316583618963687e-06).
serviceConnection(checkoutservice, paymentservice, 1.4636885448967852e-09, 1.4636885448967851e-06).
serviceConnection(checkoutservice, productcatalogservice, 2.0890716320822383e-09, 2.0890716320822385e-06).
serviceConnection(checkoutservice, shippingservice, 5.152219635914196e-09, 5.1522196359141965e-06).
serviceConnection(frontend, productcatalogservice, 1.1069616941586624e-07, 0.00011069616941586624).
serviceConnection(frontend, recommendationservice, 3.325635824338209e-08, 3.325635824338209e-05).
serviceConnection(frontend, shippingservice, 7.69695440139809e-09, 7.69695440139809e-06).
serviceConnection(frontend, adservice, 1.6296939699445272e-08, 1.6296939699445272e-05).
serviceConnection(checkoutservice, cartservice, 2.712488707059275e-09, 2.712488707059275e-06).
serviceConnection(frontend, cartservice, 3.5171871902859043e-08, 3.517187190285904e-05).
serviceConnection(frontend, checkoutservice, 3.6487012544123915e-09, 3.6487012544123915e-06).
serviceConnection(frontend, currencyservice, 7.372059574450011e-08, 7.372059574450011e-05).
serviceConnection(recommendationservice, productcatalogservice, 1.2377707999347731e-08, 1.237770799934773e-05).
service(frontend, 2.861262, 2861.262).
service(productcatalogservice, 1.277202, 1277.202).
service(currencyservice, 1.137168, 1137.168).
service(recommendationservice, 0.778833, 778.833).
service(cartservice, 0.705945, 705.945).
service(adservice, 0.324624, 324.624).
service(checkoutservice, 0.15506999999999999, 155.07).
service(shippingservice, 0.127671, 127.671).
service(emailservice, 0.06540900000000001, 65.409).
service(paymentservice, 0.045117, 45.117).
node(washington, 244).
node(california, 235).
node(texas, 231).
node(florida, 570).
node(newyork, 236).
node(arizona, 229).
deployedTo(frontend,large,washington).
deployedTo(productcatalogservice,large,florida).
deployedTo(recommendationservice,large,texas).
deployedTo(checkoutservice,tiny,california).
deployedTo(adservice,tiny,texas).
deployedTo(cartservice,tiny,florida).
deployedTo(shippingservice,tiny,florida).
deployedTo(currencyservice,tiny,florida).
deployedTo(paymentservice,tiny,newyork).
deployedTo(emailservice,tiny,newyork).
highConsumptionService(frontend,large,washington,0.428).
highConsumptionService(frontend,large,california,0.412).
highConsumptionService(frontend,large,florida,1.000).
highConsumptionService(frontend,large,newyork,0.414).
highConsumptionService(productcatalogservice,large,florida,0.446).
