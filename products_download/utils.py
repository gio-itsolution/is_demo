from pandas import DataFrame, ExcelWriter, concat


def excel_table_create(products: dict) -> DataFrame:
    """
    Принимает массив из товаров. Создает датафрейм и сохраняет его в виде excel-файла.
    Возвращает датафрейм.
    """
    products_df = DataFrame(columns=['id', 'Название',
                                     'Цена', 'Описание',
                                     'id Каталога', 'id Секции'])

    for product_id, value in products.items():
        new_line = {'id': int(product_id), 'Название': value['NAME'],
                    'Цена': value['PRICE'], 'Описание': value['DESCRIPTION'],
                    'id Каталога': value['CATALOG_ID'], 'id Секции': value['SECTION_ID']}
        products_df = concat([products_df, DataFrame([new_line])], ignore_index=True)
    products_df = products_df.set_index('id')

    writer = ExcelWriter('media/files/Products.xlsx')
    products_df.to_excel(writer, sheet_name='products')

    for column in products_df:
        column_width = max(products_df[column].astype(str).map(len).max(), len(column))
        col_idx = products_df.columns.get_loc(column) + 1
        writer.sheets['products'].set_column(col_idx, col_idx, column_width)

    writer.close()

    return products_df
