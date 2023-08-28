---
title: Activity之间转场动画
date: 2019-09-27 14:26:50
tags: Android
---

# Activity之间转场动画

Activity之间切换的动画是常见需求，网上搜了一下，大致有五种。肯定还有别的，我也没有别的时间去整理，写写demo当熟悉Android。整理一下如下：

<!--more-->

## 利用Theme
- 在Manifest.xml文件中设置style theme，其名称为`AppTheme`

```
<application
	android:theme="@style/AppTheme">
</application>
```

- 在values文件夹中的styles.xml文件中，针对style文件进行配置，基中可以看到也有一个`AppTheme`的style，说明是对应关系；
- 在这里把名为`windowAnimationStyle`的样式改成`Animation_Fade`；

```
<style name="AppTheme" parent="Theme.AppCompat.Light.DarkActionBar">
        <!-- Customize your theme here. -->
        <item name="colorPrimary">@color/colorPrimary</item>
        <item name="colorPrimaryDark">@color/colorPrimaryDark</item>
        <item name="colorAccent">@color/colorAccent</item>
        <item name="android:windowAnimationStyle">@style/Animation_Fade</item>
    </style>
    
```

- 接着AppTheme的style，在其下面继续创建`Animation_Fade`的style，供AppTheme调用动画样式。

```
    <style name="Animation_Fade"
        parent="@android:style/Animation.Activity">
        <item name="android:activityOpenEnterAnimation">@anim/fade_in</item>
        <item name="android:activityCloseExitAnimation">@anim/fade_out</item>
    </style>

```

- 这里的item有4种：

属性 | 作用
---- | ----
activityOpenEnterAnimation | 用于设置打开新的Activity并进入新的Activity展示的动画
activityOpenExitAnimation | 用于设置打开新的Activity并销毁之前的Activity展示的动画
activityCloseEnterAnimation | 用于设置关闭当前Activity进入上一个Activity展示的动画
activityCloseExitAnimation | 用于设置关闭当前Activity时展示的动画

- 可以注意到上方有`fade_in`和`fade_out`两种动画关键字，我们在anim的文件夹中创建同样名称的两个xml文件，如果没有anim文件夹则自行创建。
- 其中的内容如下


```
<set xmlns:android="http://schemas.android.com/apk/res/android">
	 <alpha
	        android:fromAlpha="1.0"
	        android:toAlpha="0.0"
	        android:duration="300"
	        android:interpolator="@android:anim/accelerate_interpolator">

    </alpha>
    <translate
        android:fromXDelta="0.0"
        android:toXDelta="100%p"
        android:duration="300"
        android:interpolator="@android:anim/accelerate_interpolator"
        >
    </translate>
</set>

/*
解释：
translate//位移
rotate//旋转
scale//缩放
alpha//透明
set//设置
*/
```

以上是全局采用相同的动画，如果要单独设置某个activity的动画，可以在Manifest.xml文件中进行配置。

```
<activity
android:name=".View.xxxActivity"
android:label="@string/xxxActivity"
android:theme="@style/AppTheme" /> 
```

#### 这种方式最好还是适用于全局统一转场动画的场景，如果单个activity需要单独使用，采用了这种方式的话仍然会受到影响。例如：A，B，C三个activity，AC采用统一theme，B单独应用不同theme，从A到C的动画是期望的样式，B到C的动画进入的时候会是期望的样子，但C到B返回的时候会是统一theme的样式。

## 利用overridePendingTransition

```
startActivity(intent);
overridePendingTransition(R.anim.fade_in, R.anim.fade_out);

```

跳转后调用`overridePendingTransition `方法，传入两个anim样式，一个是进入的样式，一个是返回的样式，较上种办法更为灵活。

## 利用ActivityOptions自带的效果

在将要显示的activity中的onCreate方法中使用以下代码

```
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        getWindow().requestFeature(Window.FEATURE_ACTIVITY_TRANSITIONS);
        Transition explode = TransitionInflater.from(this).inflateTransition(android.R.transition.explode);
        getWindow().setEnterTransition(explode);

        setContentView(R.layout.activity_third);
    }
```
其中`requestFeature`方法必须在`setContentView`之前调用。
接着在跳转发起方使用以下代码。

```
        Intent itnt = new Intent(this, ThirdAcitivity.class);
        startActivity(itnt, ActivityOptions.makeSceneTransitionAnimation(MainActivity.this).toBundle());
```

## 利用ActivityOptions通过style形式处理
先在res创建个文件夹`transition`，再创建一个资源文件`explode`，内容改成以下：

```
<?xml version="1.0" encoding="utf-8"?>
<transitionSet xmlns:android="http://schemas.android.com/apk/res/android"
    >
    <explode
        android:interpolator="@android:interpolator/bounce"></explode>
</transitionSet>
```
再去到values文件夹中的styles文件将app theme主题中增添以下

```
<item name="android:windowEnterTransition">@transition/explode</item>
<item name="android:windowExitTransition">@transition/explode</item>
```
如此整个项目如果没有特别指定的情况下，过度动画则变成explode的样式。

## 共享组件过渡动画
从一个view跳转到下一个activity的view，通过对这两个view采用相同的transitionName执行过渡动画。
比如点击某个button则跳转到其它activity，则将此button和transitionName和activity的view进行绑定相同的transitionName即可，代码如下：

xml文件中找到button并增加：

```
    <Button
        android:id="@+id/fifth_button"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="组件共享过渡动画"
        app:layout_constraintLeft_toLeftOf="parent"
        app:layout_constraintRight_toRightOf="parent"
        app:layout_constraintTop_toBottomOf="@+id/fourth_button"
        android:layout_marginTop="20dp"
        android:transitionName="sharedTransitionName"
        />
```
xml文件中找到activity最上层的路径添加

```
<?xml version="1.0" encoding="utf-8"?>
<android.support.constraint.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".FifthActivity"
    android:transitionName="sharedTransitionName">

</android.support.constraint.ConstraintLayout>
```
最后在跳转触发的地方更新以下代码：

```
Intent itnt = new Intent(this, FifthActivity.class);
startActivity(itnt, ActivityOptions.makeSceneTransitionAnimation(MainActivity.this, btn, "sharedTransitionName").toBundle());
```

以上则是五种过渡动画的方法，各有自适应的业务场景，视实际情况自行选择。

作为一个资深iOS让我来做Android，权当增长见识了，加个油。

[Android官方说明 -- Start an activity using an animation](https://developer.android.com/training/transitions/start-activity)

[参考链接 -- Android Activity 跳转动画设置](https://www.jianshu.com/p/07441dedde03)
