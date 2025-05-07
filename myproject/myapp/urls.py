from django.urls import path
from .import views

urlpatterns = [ 
    path("",views.show_all,name='home1'), 
    path("",views.show,name='home'), 

    # path("",views.get_all_products,name='show_products'), 

    path("about_us/",views.about_us,name="about_us"),
    path("product/",views.productview,name="product"),
    path("register/",views.registerview,name="register"),
    path("login/",views.loginview,name="login"),
    path("my_order/",views.my_order,name="my_order"),
    path("my_account/",views.my_account,name="my_account"),
    path("logout/",views.logoutview,name="logout"),
    path('cat/<int:id>/',views.cat_view,name="cat"),
    path('search/',views.searchview,name="search1"),
    path('add_to_cart2/',views.show_cart,name="add_to_cart2"),
    path('show/<int:id>/',views.show_data,name="show_product"),


    path('cart2/',views.show_cart,name='show_cart'),
    path('add_cart/<int:id>',views.store_cart,name='addcart'),
    path('increase_cart/<int:id>',views.increase_cart,name='increase_cart'),
    path('decrease_cart/<int:id>',views.decrease_cart,name='decrease_cart'),
    path('delete_cart/<int:id>',views.delete_cart,name='delete_cart'), 


    path('checkout1/<int:id>/',views.checkout_direct,name='checkout_direct'),
    path('checkout/',views.checkout,name='checkout'),
    path('orders/',views.order,name='orders'),

    # path('product/<int:id>/',views.product_detail,name='product_detail'),

    path('profile/', views.profile, name='profile'),

    path("contact_us/",views.contact_view,name="contact"),

    path('update/<int:id>/',views.updatedata,name="update"),
    path('delete1/<int:id>/',views.deleteview,name="delete1"),
    path('product_1/',views.show_product,name="product1"),
    path('search/',views.searchview_for_admin,name="search2"),

    path("product/",views.productview,name="product"),

    path('cat/<int:id>/',views.cat_view_for_update,name="cat1"),

    path("orders_delete/<int:id>/",views.orders_delete,name="cancel"),

    # path('cart/', views.cart_view, name='cart_view'),




# ---------------Rest-api-------------------
    path("drf_curd/",views.crudapi_view.as_view(),name="crud"),


    path("user_orders/",views.admin_orders,name="admin_orders"),

    path("user_details/",views.customer_details,name="admin_user_details"),

#--------------- Review -------------------

    path('add_rating/<int:id>',views.rating,name='add_rating'),



]
