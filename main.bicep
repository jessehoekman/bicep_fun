param location string = resourceGroup().location

@minLength(3)
@maxLength(24)
@description('Provide a name for the storage account. Use only lower case letters and numbers. The name must be unique across Azure.')
param storageAccountName string = 'store${uniqueString(resourceGroup().id)}'

resource virtualNetwork 'Microsoft.Network/virtualNetworks@2023-09-01' = {
  name: 'vn-jazuru'
  location: location
  properties: {
    addressSpace: {
      addressPrefixes: [
        '10.0.0.0/16'
      ]
  }
  subnets: [
    {
      name: 'subnet-jazuru'
      properties: {
        addressPrefix: '10.0.0.0/24'
      }
    }
    {
      name: 'subnet-jazuru2'
      properties: {
        addressPrefix: '10.0.1.0/24'
      }
    }
  ]
}
}

resource exampleStorage 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: storageAccountName
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
}
