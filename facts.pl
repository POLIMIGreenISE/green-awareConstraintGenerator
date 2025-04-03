serviceConnection(load_balancer, frontend, 0.005, 5.0).
serviceConnection(frontend, api, 0.005, 5.0).
serviceConnection(frontend, redis, 0.003, 3.0).
serviceConnection(api, identity_provider, 0.003, 3.0).
serviceConnection(api, etcd, 0.004, 4.0).
serviceConnection(api, database, 0.011, 11.0).
serviceConnection(api, redis, 0.001, 1.0).
serviceConnection(identity_provider, etcd, 0.001, 1.0).
service(load_balancer, 0.747, 1494.0).
service(frontend, 0.594, 1188.0).
service(api, 1.2274449947122323, 2454.8899894244646).
service(identity_provider, 0.8839999999999996, 1767.999999999999).
service(database, 1.360999999999997, 2721.999999999994).
service(redis, 0.08800000000000016, 176.0000000000003).
service(etcd, 0.045, 90.0).
node(public1, 402).
node(public2, 255).
node(private1, 346).
node(private2, 74).
node(private3, 620).
node(private4, 155).
node(private5, 290).
deployedTo(load_balancer,large,public1).
deployedTo(api,large,private1).
deployedTo(frontend,large,public1).
deployedTo(identity_provider,large,private3).
deployedTo(redis,large,private3).
deployedTo(database,large,private5).
deployedTo(etcd,large,private2).
highConsumptionConnection(api,large,database,large,0.006).
highConsumptionConnection(load_balancer,large,frontend,large,0.003).
highConsumptionService(api,large,private3,0.910).
highConsumptionService(database,large,private3,1.000).
