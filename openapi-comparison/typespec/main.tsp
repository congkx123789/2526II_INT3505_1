import "@typespec/http";
import "@typespec/openapi3";

using TypeSpec.Http;

@service({
  title: "Quản lý Thư viện API",
})
@server("http://api.library.com", "Main server")
namespace LibraryService;

model Book {
  @key id: string;
  title: string;
  author: string;
}

@route("/books")
interface Books {
  @summary("Lấy danh sách sách")
  @get list(): Book[];
  
  @summary("Thêm sách mới")
  @post create(@body book: Book): {
    @statusCode _: 201;
    @body book: Book;
  };
}
