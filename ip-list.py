#!/usr/bin/env python3

import sys
import argparse
import netaddr
import lxml.etree


def main(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file')
    arguments = parser.parse_args(args)

    jnmfile = arguments.file

    e = lxml.etree.parse(jnmfile).getroot()

    # interfaces = e.findall(".//PhysicalIF")
    # for interface in interfaces:
    #deviceNodes = e.findall(".//device")
    deviceNodes = e.findall("layout/locations/org.apache.commons.collections15.map.LazyMap/map/entry/ch.rakudave.jnetmap.model.device.Host")
    i = 0
    for deviceNode in deviceNodes:
        if "reference" in deviceNode.attrib:
            deviceNode = deviceNode.find(deviceNode.attrib["reference"])
            #continue
        #else:
        #    continue

        if deviceNode is not None:
            i+=1
            name = "None"
            type = "None"
            location = "None"
            if deviceNode.find("name") is not None:
                name = deviceNode.find("name").text
            if deviceNode.find("type") is not None:
                type = deviceNode.find("type").text
            if deviceNode.find("location") is not None:
                location = deviceNode.find("location").text
            print("[{type}] {name} ({location})".format(name=name, type=type, location=location))

            interfaceNodes = deviceNode.findall("interfaces/PhysicalIF")
            for interfaceNode in interfaceNodes:
                if "reference" in interfaceNode.attrib:
                    interfaceNode = interfaceNode.find(str(interfaceNode.attrib["reference"]))
                for address in getAddressOfPhysicalIF(interfaceNode):
                    print("\t -", address)
    print(i)

def getAddressOfPhysicalIF(physicalIF):
    addressNodes = physicalIF.findall("address")
    for addressNode in addressNodes:
        if "reference" in addressNode.attrib:
            addressNode = addressNode.find(str(addressNode.attrib["reference"]))
        defaultAddressNodes = addressNode.findall("java.net.InetAddress/default/address")
        addresses = []
        for defaultAddressNode in defaultAddressNodes:
            addresses.append(netaddr.IPAddress(int(defaultAddressNode.text) + 2**32))
        return addresses


if __name__ == '__main__':
    main(sys.argv[1:])
