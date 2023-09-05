pub mod indentify{
    use hard_xml::{XmlWrite, XmlRead};

    #[derive(Debug, Clone, XmlWrite, XmlRead)]
    #[xml(tag = "s:Envelope")]
    pub struct Envelope {
        #[xml(attr = "xmlns:s")]
        pub soap_schema: String,
        #[xml(attr = "xmlns:wsmid")]
        pub wsman_schema: String,
        #[xml(child = "s:Header")]
        pub header: Header,
        #[xml(child = "s:Body")]
        pub body: Body
    }

    #[derive(Debug, Clone, XmlWrite, XmlRead)]
    #[xml(tag = "s:Header")]
    pub struct Header {}

    #[derive(Debug, Clone, XmlWrite, XmlRead)]
    #[xml(tag = "s:Body")]
    pub struct Body {
        #[xml(child = "wsmid:Identify")]
        pub identify: Identify
    }

    #[derive(Debug, Clone, XmlWrite, XmlRead)]
    #[xml(tag = "wsmid:Identify")]
    pub struct Identify{}
}

pub mod identify_response{
    use hard_xml::{XmlWrite, XmlRead};

    #[derive(XmlWrite, XmlRead, Debug, Clone)]
    #[xml(tag = "s:Envelope")]
    pub struct Envelope{
        #[xml(attr = "xml:lang")]
        language: String,
        #[xml(attr = "xmlns:s")]
        soap_schema: String,
        #[xml(child = "s:Header")]
        header: Header,
        #[xml(child = "s:Body")]
        body: Body
    }

    #[derive(XmlWrite, XmlRead, Debug, Clone)]
    #[xml(tag = "s:Header")]
    pub struct Header{}

    #[derive(XmlWrite, XmlRead, Debug, Clone)]
    #[xml(tag = "s:Body")]
    pub struct Body{
        #[xml(child = "wsmid:IdentifyResponse")]
        identify_response: IdentifyResponse
    }
    #[derive(XmlWrite, XmlRead, Debug, Clone)]
    #[xml(tag = "wsmid:IdentifyResponse")]
    pub struct IdentifyResponse{
        #[xml(attr = "xmlns:wsmid")]
        wsmid: String,
        #[xml(child = "wsmid:ProtocolVersion")]
        protocol_version: ProtocolVersion,
        #[xml(child = "wsmid:ProductVendor")]
        product_vendor: ProductVendor,
        #[xml(child = "wsmid:ProductVersion")]
        product_version: ProductVersion,
        #[xml(child = "wsmid:SecurityProfiles")]
        security_profiles: SecurityProfiles
    }
    #[derive(XmlWrite, XmlRead, Debug, Clone)]
    #[xml(tag="wsmid:ProtocolVersion")]
    pub struct ProtocolVersion{
        #[xml(text)]
        protocol_version: String
    }
    #[derive(XmlWrite, XmlRead, Debug, Clone)]
    #[xml(tag="wsmid:ProductVendor")]
    pub struct ProductVendor{
        #[xml(text)]
        product_vendor: String
    }
    #[derive(XmlWrite, XmlRead, Debug, Clone)]
    #[xml(tag="wsmid:ProductVersion")]
    pub struct ProductVersion{
        #[xml(text)]
        product_version: String
    }
    #[derive(XmlWrite, XmlRead, Debug, Clone)]
    #[xml(tag="wsmid:SecurityProfiles")]
    pub struct SecurityProfiles{
        #[xml(child="wsmid:SecurityProfileName")]
        security_profile: Vec<SecurityProfileName>
    }
    #[derive(XmlWrite, XmlRead, Debug, Clone)]
    #[xml(tag="wsmid:SecurityProfileName")]
    pub struct SecurityProfileName {
        #[xml(text)]
        profile_name: String
    }
}

pub mod wmi_query{
    use hard_xml::{XmlWrite, XmlRead};

    #[derive(XmlWrite, XmlRead, Debug, Clone)]
    #[xml(tag = "s:Envelope")]
    pub struct Envelope{
        #[xml(attr = "xmlns:s")]
        pub soap_scheme: String,
        #[xml(attr = "xmlns:a")]
        pub soap_address: String,
        #[xml(attr = "xmlns:w")]
        pub wsman_scheme: String,
        #[xml(attr = "xmlns:p")]
        pub microsoft_wsman_scheme: String,
        #[xml(child = "s:Header")]
        pub header: Header,
        #[xml(child = "s:Body")]
        pub body: Body
    }
    #[derive(XmlWrite, XmlRead, Debug, Clone)]
    #[xml(tag = "s:Header")]
    pub struct Header{
        #[xml(child = "a:To")]
        pub receiver: To,
        #[xml(child = "a:ReplyTo")]
        pub reply_to: ReplyTo,
        #[xml(child = "w:ResourceUri")]
        pub reource_uri: ResourceUri,
        #[xml(child = "a:Action")]
        pub action: Action,
        #[xml(child = "w:MaxEnvelopeSize")]
        pub max_envelop_size: MaxEnvelopeSize,
        #[xml(child = "a:MessageID")]
        pub message_id: MessageId,
        #[xml(child = "w:Locale")]
        pub locale: Locale,
        #[xml(child = "a:DataLocale")]
        pub data_locale: DataLocale,
        #[xml(child = "p:SessionId")]
        pub session_id: SessionId,
        #[xml(child = "p:OperationId")]
        pub operation_id: OperationId,
        #[xml(child = "p:SequenceId")]
        pub sequence_id: SequenceId,
        #[xml(child = "w:SelectorSet")]
        pub selector_set: SelectorSet,
        #[xml(child = "w:OperationTimeout")]
        pub operation_timeout: OperationTimeout
    }
    #[derive(Debug, Clone, XmlWrite, XmlRead)]
    #[xml(tag = "s:Body")]
    pub struct Body{}
    #[derive(Debug, Clone, XmlWrite, XmlRead)]
    #[xml(tag = "a:To")]
    pub struct To{
        #[xml(text)]
        pub address: String
    }
    #[derive(Debug, Clone, XmlWrite, XmlRead)]
    #[xml(tag = "a:ReplyTo")]
    pub struct ReplyTo{
        #[xml(child = "a:Address")]
        pub address: Address
    }
    #[derive(Debug, Clone, XmlWrite, XmlRead)]
    #[xml(tag = "w:ResourceURI")]
    pub struct ResourceUri {
        #[xml(attr = "s:mustUnderstand")]
        pub must_understand: bool,
        #[xml(text)]
        pub uri: String
    }
    #[derive(Debug, Clone, XmlWrite, XmlRead)]
    #[xml(tag = "a:Action")]
    pub struct Action{
        #[xml(attr = "s:mustUnderstand")]
        pub must_understand: bool,
        #[xml(text)]
        pub action: String
    }
    #[derive(Debug, Clone, XmlWrite, XmlRead)]
    #[xml(tag = "w:MaxEnvelopeSize")]
    pub struct MaxEnvelopeSize{
        #[xml(attr = "s:mustUnderstand")]
        pub must_understande: bool,
        #[xml(text)]
        pub max_envelop_size: u32
    }
    #[derive(Debug, Clone, XmlWrite, XmlRead)]
    #[xml(tag = "a:MessageID")]
    pub struct MessageId{
        #[xml(text)]
        pub uuid: String
    }
    #[derive(Debug, Clone, XmlWrite, XmlRead)]
    #[xml(tag = "w:Locale")]
    pub struct Locale {
        #[xml(attr = "xml:lang")]
        pub locale: String,
        #[xml(attr = "s:mustUnderstand")]
        pub must_understand: bool
    }
    #[derive(Debug, Clone, XmlWrite, XmlRead)]
    #[xml(tag = "p:DataLocale")]
    pub struct DataLocale{
        #[xml(attr = "xml:lang")]
        pub language: String,
        #[xml(attr = "s:mustUnderstand")]
        pub must_understand: bool
    }
    #[derive(Debug, Clone, XmlWrite, XmlRead)]
    #[xml(tag = "p:SessionId")]
    pub struct SessionId{
        #[xml(attr = "s:mustUnderstand")]
        pub must_understand: bool,
        #[xml(text)]
        pub session_id: String
    }
    #[derive(Debug, Clone, XmlWrite, XmlRead)]
    #[xml(tag = "p:OperationId")]
    pub struct OperationId{
        #[xml(attr = "s:mustUnderstand")]
        pub must_understand: bool,
        #[xml(text)]
        pub operation_id: String
    }
    #[derive(Debug, Clone, XmlWrite, XmlRead)]
    #[xml(tag = "p:SequenceId")]
    pub struct SequenceId {
        #[xml(attr = "s:mustUnderstand")]
        pub must_understand: bool,
        #[xml(text)]
        pub sequence_id: u8
    }
    #[derive(Debug, Clone, XmlWrite, XmlRead)]
    #[xml(tag = "w:SelectorSet")]
    pub struct SelectorSet{
        #[xml(child = "w:Selector")]
        pub selector_set: Vec<Selector>
    }
    #[derive(Debug, Clone, XmlRead, XmlWrite)]
    #[xml(tag = "w:OperationTimeout")]
    pub struct OperationTimeout{
        #[xml(text)]
        pub operation_timeout: String
    }
    #[derive(Debug, Clone, XmlRead, XmlWrite)]
    #[xml(tag = "a:Address")]
    pub struct Address {
        #[xml(attr = "mustUnderstand")]
        pub must_understand: bool,
        #[xml(text)]
        pub address: String
    }
    #[derive(Debug, Clone, XmlRead, XmlWrite)]
    #[xml(tag = "w:Selector")]
    pub struct Selector{
        #[xml(attr = "Name")]
        pub selector_name: String,
        #[xml(text)]
        pub selector_value: String
    }

}