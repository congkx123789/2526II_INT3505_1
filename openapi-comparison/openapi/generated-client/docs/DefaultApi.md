# DefaultApi

All URIs are relative to *http://localhost*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**booksGet**](#booksget) | **GET** /books | Lấy danh sách sách|
|[**booksPost**](#bookspost) | **POST** /books | Thêm sách mới|

# **booksGet**
> Array<Book> booksGet()


### Example

```typescript
import {
    DefaultApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new DefaultApi(configuration);

const { status, data } = await apiInstance.booksGet();
```

### Parameters
This endpoint does not have any parameters.


### Return type

**Array<Book>**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Thành công |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **booksPost**
> booksPost(book)


### Example

```typescript
import {
    DefaultApi,
    Configuration,
    Book
} from './api';

const configuration = new Configuration();
const apiInstance = new DefaultApi(configuration);

let book: Book; //

const { status, data } = await apiInstance.booksPost(
    book
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **book** | **Book**|  | |


### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**201** | Tạo thành công |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

