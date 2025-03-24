serviceConnection(checkoutservice, currencyservice, 3.4794820030169804e-06, 0.00347948200301698).
serviceConnection(checkoutservice, emailservice, 5.316583618963687e-06, 0.0053165836189636865).
serviceConnection(checkoutservice, paymentservice, 1.4636885448967853e-06, 0.0014636885448967853).
serviceConnection(checkoutservice, productcatalogservice, 2.089071632082238e-06, 0.002089071632082238).
serviceConnection(checkoutservice, shippingservice, 5.152219635914196e-06, 0.005152219635914196).
serviceConnection(frontend, productcatalogservice, 0.00011069616941586624, 0.11069616941586624).
serviceConnection(frontend, recommendationservice, 3.32563582433821e-05, 0.0332563582433821).
serviceConnection(frontend, shippingservice, 7.69695440139809e-06, 0.007696954401398091).
serviceConnection(frontend, adservice, 1.629693969944527e-05, 0.01629693969944527).
serviceConnection(checkoutservice, cartservice, 2.712488707059275e-06, 0.002712488707059275).
serviceConnection(frontend, cartservice, 3.517187190285905e-05, 0.035171871902859045).
serviceConnection(frontend, checkoutservice, 3.6487012544123915e-06, 0.0036487012544123916).
serviceConnection(frontend, currencyservice, 7.372059574450012e-05, 0.07372059574450013).
serviceConnection(recommendationservice, productcatalogservice, 1.237770799934773e-05, 0.012377707999347731).
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
highConsumptionConnection(frontend,large,productcatalogservice,medium,0.000).
highConsumptionConnection(frontend,large,currencyservice,small,0.000).
highConsumptionConnection(frontend,large,cartservice,small,0.000).
highConsumptionConnection(frontend,large,recommendationservice,large,0.000).
highConsumptionService(productcatalogservice,medium,node_c,0.799).
highConsumptionService(currencyservice,small,node_c,1.000).
