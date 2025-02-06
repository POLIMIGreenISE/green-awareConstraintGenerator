serviceConnection(checkoutservice, currencyservice, 27.988083361767835, 97.86043133485258).
serviceConnection(checkoutservice, emailservice, 42.765269485039155, 149.52891428335369).
serviceConnection(checkoutservice, paymentservice, 11.773544733013516, 41.166240325222084).
serviceConnection(checkoutservice, productcatalogservice, 16.8039699405615, 58.755139652312934).
serviceConnection(checkoutservice, shippingservice, 41.44316669638481, 144.90617726008674).
serviceConnection(frontend, productcatalogservice, 165.0064775355256, 3113.329764821238).
serviceConnection(frontend, recommendationservice, 49.57275900654144, 935.3350755951216).
serviceConnection(frontend, shippingservice, 11.473272654584028, 216.4768425393213).
serviceConnection(frontend, adservice, 24.292625739485604, 458.3514290468982).
serviceConnection(checkoutservice, cartservice, 21.818581037408045, 76.28874488604212).
serviceConnection(frontend, cartservice, 52.42807155519927, 989.2088972679107).
serviceConnection(frontend, checkoutservice, 5.438845307358472, 102.61972278034852).
serviceConnection(frontend, currencyservice, 109.88976303164551, 2073.3917553140664).
serviceConnection(recommendationservice, productcatalogservice, 99.56318871975333, 348.123037481655).
service(frontend, 167.80192880894654, 3166.074128470689).
service(productcatalogservice, 404.19326709084027, 1413.2631716462947).
service(currencyservice, 434.11738374921305, 1258.3112572440957).
service(recommendationservice, 246.47554168264722, 861.8025932959694).
service(cartservice, 269.4966763669381, 781.1497865708351).
service(adservice, 123.9262110631011, 359.20640887855393).
service(checkoutservice, 49.07465688886849, 171.58970940163806).
service(shippingservice, 48.73879717037921, 141.27187585617162).
service(emailservice, 24.970087052794554, 72.37706392114364).
service(paymentservice, 17.223553602117935, 49.92334377425488).
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
highConsumptionConnection(frontend,large,productcatalogservice,medium,0.380).
highConsumptionConnection(frontend,large,currencyservice,small,0.253).
highConsumptionConnection(recommendationservice,large,productcatalogservice,medium,0.172).
highConsumptionService(productcatalogservice,medium,node_b,0.931).
highConsumptionService(currencyservice,small,node_b,1.000).
