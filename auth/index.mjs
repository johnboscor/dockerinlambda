import { SecretsManagerClient, GetSecretValueCommand } from "@aws-sdk/client-secrets-manager"; 

const client = new SecretsManagerClient();
const input = { 
  SecretId: process.env.SECRET_ID
};

const command = new GetSecretValueCommand(input);
const response = await client.send(command);

var apiToken = response['SecretString'] //Get the apiToken from secrets manager

export const handler =  function(event, context, callback) {
    var token = event.authorizationToken;
    var tmp = event.methodArn.split(':');
    var apiGatewayArnTmp = tmp[5].split('/');
    
    // Create wildcard resource. This is to resolve unauthorized issue while using proxy resource in API gateway.
    var resource = tmp[0] + ":" + tmp[1] + ":" + tmp[2] + ":" + tmp[3] + ":" + tmp[4] + ":" + apiGatewayArnTmp[0] + '/*/*'; 

    switch (token) {
        case apiToken:
            callback(null, generatePolicy('user', 'Allow', resource));
            break;
        case 'deny':
            callback(null, generatePolicy('user', 'Deny', resource));
            break;
        case 'unauthorized':
            callback("Unauthorized");   // Return a 401 Unauthorized response
            break;
        default:
            callback("Error: Invalid token"); // Return a 500 Invalid token response
    }
};

// Help function to generate an IAM policy
var generatePolicy = function(principalId, effect, resource) {
    var authResponse = {};
    
    authResponse.principalId = principalId;
    if (effect && resource) {
        var policyDocument = {};
        policyDocument.Version = '2012-10-17'; 
        policyDocument.Statement = [];
        var statementOne = {};
        statementOne.Action = 'execute-api:Invoke'; 
        statementOne.Effect = effect;
        statementOne.Resource = resource;
        policyDocument.Statement[0] = statementOne;
        authResponse.policyDocument = policyDocument;
    }
    
    // Optional output with custom properties of the String, Number or Boolean type.
    authResponse.context = {
        "stringKey": "stringval",
        "numberKey": 123,
        "booleanKey": true
    };
    return authResponse;
}
