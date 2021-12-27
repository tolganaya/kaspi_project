from decimal import Decimal
from uuid import uuid4

from account.account import Account
import xml
import xml.etree.ElementTree as ET


class TestXMLMethods:
    def test_xml(self) -> None:
        xml_string = """
            <customer id="43433" name="Bill Gates">
              <account id="9349834894389" balance="200" currency="KZT" />
              <account id="45624352345234" balance="300" currency="USD" />
              <account id="34562346513465134" balance="1" currency="BTC" />
              <football>Barca</football>
            </customer>
        """
        root = ET.fromstring(xml_string)
        print()
        print("Root element is", root.tag, root.attrib["name"])
        if root.tag == "customer":
            for child in root:
                assert isinstance(child, ET.Element)
                print("  Child element", child.tag)
                if child.tag == "account":
                    print(f"    Balance: {child.attrib['balance']} {child.attrib['currency']}")
                if child.tag == "football":
                    print(f"    Team: {child.text}")

    def test_to_xml(self) -> None:
        root = ET.Element("customer", id="3232")
        root.attrib["name"] = "Bill Gates"
        ET.SubElement(root, "account", attrib={
            "id": "9349834894389",
            "balance": "200",
            "currency": "KZT",
        })
        ET.SubElement(root, "account", attrib={
            "id": "9349834894389",
            "balance": "300",
            "currency": "USD",
        })
        ET.SubElement(root, "account", attrib={
            "id": "9349834894389",
            "balance": "1",
            "currency": "BTC",
        })
        ET.SubElement(root, "football").text="Barca"
        xml_string = xml.etree.ElementTree.tostring(root, encoding="utf8", method="xml")
        print(xml_string)

    def test_account_from_xml(self) -> None:
        account_id = uuid4()
        xml_string = f"""
            <account id="{account_id}" currency="KZT" balance="200.0">
            </account>
        """
        account = Account.from_xml(xml_string)
        assert account.id_ == account_id
        assert account.currency == "KZT"
        assert account.balance == Decimal(200)

    def test_account_to_xml(self) -> None:
        account = Account.random()
        xml_string = account.to_xml()
        account2 = Account.from_xml(xml_string)
        assert account == account2