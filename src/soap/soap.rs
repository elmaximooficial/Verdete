/*
    Base SOAP Message:
    <s:Envelope xmlns="http://www.w3.org/2003/05/soap-envelop"
                xmlns:wsa="http://schemas.xmlsoap.org/ws/2004/08/addressing">
        <s:Header>
            <wsa:MessageID>
                // Message ID
            </wsa:MessageID>
            <wsa:From>
                <wsa:Address>addres_of_the_sender</wsa:Address>
            </wsa:From>
            <wsa:ReplyTo>
                <wsa:Address>addres_to_reply_for</wsa:Address>
            </wsa:ReplyTo>
            <wsa:To>
                address_of_the_receiver
            </wsa:To>
            <wsa:Action>action_of_the_soap_message</wsa:Action>
        </s:Header>
        <s:Body>
            // Body to be sent to the endpoint
        </s:Body>
    </s:Envelope>
*/

/*
    Endpoint Reference Base
    <wsa:EndpointReference>
        <wsa:Address>address_of_the_resource</wsa:Address>
        <wsa:ReferenceProperties></wsa:ReferenceProperties> (Optional)
        <wsa:ReferenceParameters></wsa:ReferenceParameters> (Optional)
        <wsa:PortType>xs:QName</wsa:PortType>
        <wsa:ServiceName PortName="xs:NCName" (Optional)>xs:QName</wsa:ServiceName> (Optional)
        <wsa:Policy></wsa:Policy> (Optional)
    </wsa:EndpointReference>
*/