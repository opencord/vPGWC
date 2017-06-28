# Virtual Packet Gateway Control Service

The `vPGWC` service is responsible for dictating QoS and bandwidth for a subscriber's session. It acts as an IP router with support for mobile specific tunneling and signaling protocols and provides access to external PDNs. The `vPGWC` service also manages policy enforcement, packet filtration for users, charging support, and lawful interception.

## Onboarding

To onboard this service in your system, you can add the service to the `mcord.yml` profile manifest:

```
xos_services:
  - name: vPGWC
    path: orchestration/xos_services/vPGWC
    keypair: mcord_rsa
    synchronizer: true
```

Once you have added the service, you will need to rebuilt and redeploy the XOS containers from source. Login to the `corddev` vm and `cd /cord/build`

```
$ ./gradlew -PdeployConfig=config/mcord_in_a_box.yml :platform-install:buildImages
$ ./gradlew -PdeployConfig=config/mcord_in_a_box.yml :platform-install:publish
$ ./gradlew -PdeployConfig=config/mcord_in_a_box.yml :orchestration:xos:publish
$ ./gradlew -PdeployConfig=config/mcord_in_a_box.yml PIprepPlatform
```

Now the new XOS images should be published to the registry on `prod`. To bring them up, login to the `prod` VM and define these aliases:

```
$ CORD_PROFILE=$( cat /opt/cord_profile/profile_name )
$ alias xos-pull="docker-compose -p $CORD_PROFILE -f /opt/cord_profile/docker-compose.yml pull"
$ alias xos-up="docker-compose -p $CORD_PROFILE -f /opt/cord_profile/docker-compose.yml up -d"
$ alias xos-teardown="pushd /opt/cord/build/platform-install; ansible-playbook -i inventory/head-localhost --extra-vars @/opt/cord/build/genconfig/config.yml teardown-playbook.yml; popd"
$ alias compute-node-refresh="pushd /opt/cord/build/platform-install; ansible-playbook -i /etc/maas/ansible/pod-inventory --extra-vars=@/opt/cord/build/genconfig/config.yml compute-node-refresh-playbook.yml; popd"
```

To pull new images from the database and launch the containers, while retaining the existing XOS database, run:

```
$ xos-pull; xos-up
```

Alternatively, to remove the XOS database and reinitialize XOS from scratch, run:

```
$ xos-teardown; xos-pull; xos-launch; compute-node-refresh
```