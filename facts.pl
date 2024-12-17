serviceConnection(checkoutservice, currencyservice, 27.21260954358774, 55.08625413681729).
serviceConnection(checkoutservice, emailservice, 63.015458921443596, 127.56165773571578).
serviceConnection(checkoutservice, paymentservice, 19.443780602848772, 39.35987976285177).
serviceConnection(checkoutservice, productcatalogservice, 13.558988833183731, 27.447345816161402).
serviceConnection(checkoutservice, shippingservice, 32.27967121309966, 65.34346399412887).
serviceConnection(frontend, productcatalogservice, 957.5440428711133, 1938.348264921282).
serviceConnection(frontend, recommendationservice, 1091.4287161018165, 2209.36987065145).
serviceConnection(frontend, shippingservice, 62.52837389693691, 126.57565566181562).
serviceConnection(frontend, adservice, 191.0165211502909, 386.673119737431).
serviceConnection(checkoutservice, cartservice, 65.19150127357206, 131.9666017683645).
serviceConnection(frontend, cartservice, 1274.1802613668633, 2579.3122699734076).
serviceConnection(frontend, checkoutservice, 768.1781030346295, 1555.0164029041084).
serviceConnection(frontend, currencyservice, 926.4368403644603, 1875.3782193612556).
serviceConnection(recommendationservice, productcatalogservice, 80.17492551950231, 162.2974200799642).
service(frontend, 1413.463428, 2861.262).
service(productcatalogservice, 630.937788, 1277.202).
service(currencyservice, 561.760992, 1137.168).
service(recommendationservice, 384.743502, 778.833).
service(cartservice, 348.73683, 705.945).
service(adservice, 160.364256, 324.624).
service(checkoutservice, 76.60458, 155.07).
service(shippingservice, 63.06947400000001, 127.671).
service(emailservice, 32.312046, 65.409).
service(paymentservice, 22.287798, 45.117).
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
highConsumptionConnection(frontend,large,cartservice,small,0.9014596600987282).
highConsumptionConnection(frontend,large,recommendationservice,large,0.772166222684763).
highConsumptionConnection(frontend,large,productcatalogservice,medium,0.6774452199488484).
highConsumptionConnection(frontend,large,currencyservice,small,0.655437432629817).
highConsumptionConnection(frontend,large,checkoutservice,large,0.5434722171210146).
highConsumptionService(frontend,large, node_b, 1.0).
