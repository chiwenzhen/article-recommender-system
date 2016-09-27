define("build",
function(require, exports) {
    function showBox(a, b, c, d) {
        var e = '<div id="' + a + '" class="modal fade" role="dialog"><div class="modal-dialog"><div class="modal-content"><div class="modal-header"><button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">×</span><span class="sr-only">Close</span></button><h4 class="modal-title">' + b + '</h4></div><div class="modal-body">' + c + '</div><div class="modal-footer">' + d + "</div></div></div></div>";
        $("#" + a).length > 0 && $("#" + a).remove(),
        $("body").append(e),
        $("#" + a).modal()
    }
    function showBoxContent(a, b, c) {
        var d = '<div id="' + a + '" class="modal fade" role="dialog"><div class="modal-dialog"><div class="modal-content"><div class="modal-body modal-body-alert"><div class="modal-alert-title">' + b + '</div> <i class="icon icon-alert-close" data-dismiss="modal"></i>' + c + "</div></div></div></div>";
        $("#" + a).length > 0 && $("#" + a).remove(),
        $("body").append(d),
        $("#" + a).modal()
    }
    function addTaobaoParams(a) {
        return a.tb_appkey = pointman.getConfig() ? pointman.getConfig().appkey: "",
        a.tb_scene = pointman.getConfig() ? pointman.getConfig().scene: "",
        a.tb_token = pointman.getConfig() ? pointman.getConfig().token: "",
        a
    }
    function tab_switch() {
        $(".ordinary-login ul li:first-child").addClass("active"),
        $(".ordinary-login ul li:last-child").removeClass("active")
    }
    function loadScript(a, b) {
        var c = document.createElement("script");
        c.type = "text/javascript",
        c.readyState ? c.onreadystatechange = function() { ("loaded" == c.readyState || "complete" == c.readyState) && (c.onreadystatechange = null, b())
        }: c.onload = function() {
            b()
        },
        c.src = a,
        document.body.appendChild(c)
    }
    function delayOpen(a) {
        var a = $(".js-ver-code");
        return delayTime > 1 ? (delayTime--, a.html(delayTime + "秒后重新发送..."), a.css({
            "font-size": "12px",
            padding: "0"
        }), a.addClass("disabled"), setTimeout(function() {
            delayOpen()
        },
        1e3), void 0) : (a.removeClass("disabled"), a.html("点击获取"), a.css({
            "font-size": "16px"
        }), delayTime = 60, !1)
    }
    function dpFilterRep(a) {
        return a = a.replace(/’<q>‘/g, ""),
        a = a.replace(/’<\/q>‘/g, "")
    }
    function errorAn(a) {
        a.find("textarea").css({
            "background-color": "#fdf4eb"
        }),
        a.css({
            position: "relative"
        }).stop(!0, !0).animate({
            right: "10px"
        },
        100).animate({
            right: "-10px"
        },
        100).animate({
            right: "7px"
        },
        90).animate({
            right: "-7px"
        },
        90).animate({
            right: "4px"
        },
        80).animate({
            right: "-4px"
        },
        80).animate({
            right: "0"
        },
        70,
        function() {
            a.find("textarea").css({
                "background-color": "#fff"
            })
        })
    }
    function boxAnSuccess(a, b, c) {
        var d = '<div id="new_msg_wrap" style="position:absolute;width:100%;height:100%;right:0;padding:5px;background:#b4ffc7;border-radius:5px;overflow:hidden;">' + c + "</div>";
        a.css({
            position: "relative"
        }).append(d),
        $("#new_msg_wrap").animate({
            width: "0",
            height: "0",
            bottom: "0"
        },
        500,
        function() {
            $(this).animate({
                bottom: "-80",
                opacity: "0"
            },
            200,
            function() {
                $("#new_msg_wrap").remove(),
                b.eq(0).stop(!0, !0).animate({
                    height: "100%",
                    opacity: "1"
                },
                600)
            })
        }),
        setTimeout(function() {
            $("#new_msg_wrap").remove()
        },
        500)
    }
    function getRelatedInfo(showBox, type, weiboUrl, btn) {
        if (!btn.hasClass("disabled")) {
            btn.addClass("disabled");
            var url = "/action/weibo_related",
            param = {
                is_ajax: 1,
                huxiu_hash_code: huxiu_hash_code,
                aid: aid,
                type: type,
                url: weiboUrl
            };
            $.post(url, param,
            function(data) {
                if (data = eval("(" + data + ")"), 1 == data.result) if ("get" == type) {
                    var str = "";
                    void 0 == data.mid_urls || 0 == data.mid_urls.length || $.each(data.mid_urls,
                    function(a, b) {
                        str += '<li><a class="url" target="_blank" href="' + b + '">' + b + '</a><span class="glyphicon glyphicon-remove js-remove"></span></li>'
                    });
                    var id = "related_box",
                    title = "管理-关联微博",
                    body = '<div class="js-alert"></div><div class="relating-wrap"><a class="btn btn-default pull-right js-submit" href="javascript:void(0);">提交</a><input class="form-control js-text" type="text" /></div><div class="related-wrap"><p>已关联微博</p><ul class="js-related-wrap">' + str + "</ul></div> ",
                    footer = '<button type="button" class="btn btn-gray" data-dismiss="modal">关闭</button>';
                    showBox(id, title, body, footer)
                } else "add" == type ? ($(".js-related-wrap").prepend('<li><a class="url" href="' + weiboUrl + '">' + weiboUrl + '</a><span class="glyphicon glyphicon-remove js-remove"></span></li>'), $(".js-text").val(""), $(".js-alert").addClass("alert alert-success").html(data.msg), setTimeout(function() {
                    $(".js-alert").removeClass("alert alert-success").html("")
                },
                2e3)) : "del" == type && (btn.parents("li").remove(), $(".js-alert").addClass("alert alert-success").html(data.msg), setTimeout(function() {
                    $(".js-alert").removeClass("alert alert-success").html("")
                },
                2e3));
                else $(".js-alert").addClass("alert alert-danger").html(data.msg),
                setTimeout(function() {
                    $(".js-alert").removeClass("alert alert-danger").html("")
                },
                2e3);
                btn.removeClass("disabled")
            })
        }
    }
    function getIgnoredList(btn) {
        if (!btn.hasClass("disabled")) {
            btn.addClass("disabled");
            var url = "/admin/article_reasons",
            post_data = {
                huxiu_hash_code: huxiu_hash_code,
                is_ajax: 1
            },
            aid = btn.attr("aid");
            $.post(url, post_data,
            function(data) {
                if (data = eval("(" + data + ")"), 1 == data.result) {
                    for (var html = "",
                    i = 0; i < data.data.length; i++) html += '<label class="new-lb"><input id="' + data.data[i].id + '" name="reason" value="' + data.data[i].message + '" type="checkbox" />' + data.data[i].message + "</label>";
                    var id = "ignoreModal",
                    body = '<div class="js-alert"></div><div class="clearfix"><div class="pull-left">忽略理由如下:</div><div class="modal-manage pull-right"><a class="js-modal-manage" href="javascript:void(0);">管理</a></div></div><div class="reason-box js-reason-box">' + html + '<label class="new-lb"><textarea class="form-control js-custom-reason" placeholder="您可在此输入自定义忽略理由"></textarea></label></div><div class="reason-edit-box js-reason-edit-box"></div>',
                    title = "忽略",
                    footer = '<button class="btn btn-success article-check-ignore-conform" aid=' + aid + ">确定</button>";
                    showBox(id, title, body, footer)
                } else showBox.showBox("ignoreModal", "忽略", data.msg, '<button class="btn btn-success" data-dismiss="modal" aria-hidden="true">关闭</button>');
                btn.removeClass("disabled")
            })
        }
    }
    function delayURL() {
        var a = $("#delayTime"),
        b = a.attr("data_url"),
        c = parseInt(a.html());
        return c > 1 ? (c--, a.html(c), setTimeout(function() {
            delayURL()
        },
        1e3), void 0) : (window.top.location.href = b, !1)
    }
    window.innerWidth < 900 && ($("header").css({
        position: "relative"
    }), $(".placeholder-height").css({
        display: "none"
    })),
    $("#per_center").length > 0 && require.async(["per_center"],
    function() {}),
    $("body").on("click", ".radio-inline input",
    function() {
        var a = $(this);
        $(".radio-inline").removeClass("active"),
        a.parent(".radio-inline").addClass("active")
    }),
    Messenger.options = {
        extraClasses: "messenger-fixed messenger-on-bottom messenger-on-right",
        theme: "flat"
    };
    var showMessagePrompt = function(a, b) {
        var c = $(".message-prompt"),
        d = b ? b: "success";
        return "block" == c.css("display") ? !1 : void(a && ("error" == d && c.addClass("error"), c.empty().append("<span>" + a + "</span>").stop().css({
            top: "-50px"
        }).show().animate({
            top: "0"
        },
        50), setTimeout(function() {
            c.hide().removeClass("error")
        },
        3e3)))
    };
    window.innerWidth < 1320 ? ($(".go-top").hide(), $(".min-feedback").show()) : 0 == $("#vip-zt-body").length && ($(".min-feedback").hide(), $(".go-top,.go-feedback").show()),
    $(window).resize(function() {
        window.innerWidth < 1320 ? ($(".go-top").hide(), $(".min-feedback").show()) : 0 == $("#vip-zt-body").length && ($(".min-feedback").hide(), $(".go-top,.go-feedback").show())
    }),
    $("body").on("mouseover", ".navbar-nav li",
    function() {
        $(this).find(".nums-prompt").length > 0 && ($(this).find(".nums-prompt").hide(), localStorage.setItem("index-nums-prompt", !0), localStorage.setItem("index-topic-nums-prompt", !0))
    }),
    $("body").on("click", ".js-corpus-close",
    function() {
        $(".corpus-prompt").remove(),
        localStorage.setItem("corpus_prompt", !0)
    }),
    localStorage.getItem("corpus_prompt") && $(".corpus-prompt").remove(),
    $("body").on("click", ".js-moder-lgnbtn",
    function() {
        var a = $(this),
        b = parseInt(1e5 * Math.random()),
        c = "/user/logindo",
        d = "undefined" == typeof $("#lgn_username").val() ? "": $("#lgn_username").val(),
        e = "undefined" == typeof $("#lgn_pwd").val() ? "": $("#lgn_pwd").val(),
        f = 1 == $("#autologin").prop("checked") ? "1": "0",
        g = {
            is_ajax: "1",
            random: b,
            huxiu_hash_code: huxiu_hash_code,
            username: d,
            password: e,
            autologin: f,
            geetest_challenge: $(".geetest_challenge").val(),
            geetest_validate: $(".geetest_validate").val(),
            geetest_seccode: $(".geetest_seccode").val()
        };
        return "" == g.username ? (showMessagePrompt("帐号不能为空", "error"), !1) : "" == g.password ? (showMessagePrompt("密码不能为空", "error"), !1) : "" == g.geetest_challenge || "" == g.geetest_validate || "" == g.geetest_seccode ? (showMessagePrompt("请滑动滑块完成验证码", "error"), !1) : void(a.hasClass("disabled") || (a.addClass("disabled"), $.ajax({
            type: "post",
            url: c,
            data: g,
            dataType: "json",
            async: !0,
            success: function(b) {
                if ($.cookie("callback_url", ""), "1" == b.result) {
                    showMessagePrompt(b.msg);
                    var c = localStorage.getItem("callback_url");
                    c ? (localStorage.removeItem("callback_url"), window.location.href = c) : window.location.reload()
                } else showMessagePrompt(b.msg, "error");
                a.removeClass("disabled")
            },
            error: function(b) {
                a.removeClass("disabled"),
                Messenger().post({
                    message: g.msg,
                    type: "error",
                    showCloseButton: !0
                })
            }
        })))
    }),
    $("body").on("click", ".js-btn-logout",
    function() {
        var a = $(this),
        b = parseInt(1e5 * Math.random()),
        c = "/user/logout",
        d = {
            is_ajax: "1",
            random: b,
            huxiu_hash_code: huxiu_hash_code
        };
        a.hasClass("disabled") || $.ajax({
            type: "post",
            url: c,
            data: d,
            dataType: "json",
            async: !0,
            success: function(a) {
                "1" == a.result ? (showMessagePrompt(a.msg), "undefined" != typeof page ? window.location.href = "/": window.location.reload()) : showMessagePrompt(a.msg, "error")
            },
            error: function(a) {
                Messenger().post({
                    message: d.msg,
                    type: "error",
                    showCloseButton: !0
                })
            }
        })
    });
    var huxiu_url = window.location.href; (huxiu_url.indexOf("active") > 0 || huxiu_url.indexOf("chuangye") > 0) && ($("header").css("position", "relative"), $(".placeholder-height").remove()),
    $(".vip-zt-body").length > 0 && $(".go-top").remove();
    var menu_h1 = "70px",
    menu_h2 = "90px";
    if ($(".js-go-top").length > 0) {
        $(".js-go-top").click(function() {
            $("body, html").animate({
                scrollTop: 0
            },
            500)
        });
        var left = window.innerWidth / 2 + 587,
        left2 = window.innerWidth / 2 + 77;
        $(".js-go-top").css({
            left: left + "px"
        }),
        $(".feedback-box").css({
            left: left2 + "px"
        }),
        $(".go-feedback").css({
            left: left + "px"
        }),
        $(window).scroll(function() {
            if (window.innerWidth < 1320) $(".go-top").hide(),
            $(".min-feedback").show();
            else {
                var a = $(".js-go-top").offset().top,
                b = $(".footer").offset().top,
                c = window.innerWidth / 2 + 587,
                d = window.innerWidth / 2 + 77;
                if ($(".js-go-top").offset().top > $(window).height()) if ($(".js-go-top").fadeIn(500), a > b) {
                    var e = a - b + 140 + "px";
                    $(".go-top").css({
                        bottom: e
                    })
                } else $(".js-go-top").css({
                    bottom: "151px"
                });
                else $(".js-go-top").fadeOut(500);
                $(".js-go-top").css({
                    left: c + "px"
                }),
                $(".feedback-box").css({
                    left: d + "px"
                }),
                $(".go-feedback").css({
                    left: c + "px"
                })
            }
        })
    }
    var scroll_flag = !0;
    $(window).scroll(function() {
        huxiu_url.indexOf("active") > 0 || huxiu_url.indexOf("chuangye") > 0 || ($(window).scrollTop() > 70 ? scroll_flag && (menu_h1 = "60px", menu_h2 = "80px", scroll_flag = !1, $("header").stop().animate({
            height: "50px",
            "line-height": "50px"
        },
        300), $("header .navbar-left li,.navbar-right").css({
            height: "60px"
        }), $(".navbar-header-vip").length > 0 ? $(".container>.navbar-header").stop().animate({
            width: "65px"
        },
        300) : $(".container>.navbar-header").stop().animate({
            width: "50px"
        },
        300), $("header .navbar-left").stop().animate({
            "font-size": "16px"
        },
        300), $("header .navbar-right").stop().animate({
            "font-size": "14px",
            "margin-right": "0px"
        },
        300), $(".placeholder-height").stop().animate({
            height: "80px"
        },
        300), $("header .navbar-right li:last-child a").stop().animate({
            width: "60px",
            height: "34px",
            "line-height": "34px",
            "margin-top": "7px"
        },
        300), $("header .header-column").stop().animate({
            "margin-top": "60px"
        },
        300), $(".navbar-nav.navbar-right .user-head .avatar").stop().animate({
            "margin-top": "7px"
        },
        300)) : scroll_flag || (menu_h1 = "70px", menu_h2 = "90px", scroll_flag = !0, $("header").stop().animate({
            height: "60px",
            "line-height": "60px"
        },
        300), $("header .navbar-left li,.navbar-right").css({
            height: "80px"
        }), $(".navbar-header-vip").length > 0 ? $(".container>.navbar-header.navbar-header-vip").stop().animate({
            width: "85px"
        },
        300) : $(".container>.navbar-header").stop().animate({
            width: "63px"
        },
        300), $("header .navbar-left").stop().animate({
            "font-size": "18px"
        },
        300), $("header .navbar-right").stop().animate({
            "font-size": "16px",
            "margin-right": "10px"
        },
        300), $(".placeholder-height").stop().animate({
            height: "90px"
        },
        300), $("header .navbar-right li:last-child a").stop().animate({
            width: "70px",
            height: "40px",
            "line-height": "40px",
            "margin-top": "10px"
        },
        300), $("header .header-column").stop().animate({
            "margin-top": "70px"
        },
        300), $(".navbar-nav.navbar-right .user-head .avatar").stop().animate({
            "margin-top": "11px"
        },
        300)))
    }),
    $(document).on("mouseenter", ".js-show-menu",
    function() {
        var a = $(this),
        b = a.find(".menu-box");
        a.hasClass("active") || (a.addClass("active"), b.stop().css({
            opacity: "0",
            "margin-top": menu_h2
        }).show().animate({
            opacity: "1",
            "margin-top": menu_h1
        },
        200))
    }),
    $(document).on("mouseleave", ".js-show-menu",
    function() {
        var a = $(this),
        b = a.find(".menu-box");
        b.stop().animate({
            opacity: "0",
            "margin-top": menu_h1
        },
        300,
        function() {
            b.hide()
        }),
        a.removeClass("active")
    });
    var isOut = !0,
    is_feedback = !0;
    document.onmousedown = function() {
        is_feedback && ($(".js-modal-backdrop").hide(), $(".feedback-box").hide()),
        $(".js-qr-ds").length > 0 && isOut && ($(".js-qr-ds").css({
            opacity: "1",
            height: "48px",
            overflow: "hidden"
        }).show(), $(".js-qr-img").removeClass("info-true"), $(".js-qr-img").addClass("hide"), $(".js-qr-img").addClass("info-false"), setTimeout(function() {
            $(".js-qr-ds").addClass("transition")
        },
        600))
    },
    $("body").on("mouseover", ".feedback-box",
    function() {
        is_feedback = !1
    }),
    $("body").on("mouseout", ".feedback-box",
    function() {
        is_feedback = !0
    });
    var random = function(a) {
        return Math.floor(Math.random() * a)
    };
    $("body").on("click", ".js-show-search-box",
    function() {
        if ($("#search-box").hasClass("search-box-last")) if ($(".search-box").hasClass("active")) $("#history").addClass("hide"),
        $(".search-box").removeClass("active"),
        $(".search-box").addClass("hide"),
        $(".search-content").removeClass("overlay-dialog-animate"),
        $(document.body).removeClass("modal-open"),
        $(document.body).removeAttr("style");
        else {
            if ($.cookie("huxiu_search_history")) {
                var a = $.cookie("huxiu_search_history").split(",");
                if (a.length > 0) {
                    var b = "";
                    $.each(a,
                    function(a, c) {
                        b += '<li class="transition"><a href="/search.html?s=' + c + '">' + c + "</a></li>"
                    }),
                    $("#history").removeClass("hide"),
                    $("#history_ul").empty(),
                    $("#history_ul").append(b)
                }
            }
            $(".search-box").addClass("active"),
            $(".search-content").addClass("overlay-dialog-animate"),
            $(".search-box").removeClass("hide"),
            $(document.body).css({
                "padding-right": " 17px"
            })
        } else if ($(".search-box").hasClass("active")) $("#history").addClass("hide"),
        $(".search-box").removeClass("active"),
        $(".search-content").removeClass("overlay-dialog-animate"),
        $(document.body).removeClass("modal-open"),
        $(document.body).removeAttr("style");
        else {
            if ($.cookie("huxiu_search_history")) {
                var a = $.cookie("huxiu_search_history").split(",");
                if (a.length > 0) {
                    var b = "";
                    $.each(a,
                    function(a, c) {
                        b += '<li class="transition"><a href="/search.html?s=' + c + '">' + c + "</a></li>"
                    }),
                    $("#history").removeClass("hide"),
                    $("#history_ul").empty(),
                    $("#history_ul").append(b)
                }
            }
            $(".search-box").addClass("active"),
            $(".search-content").addClass("overlay-dialog-animate"),
            $(document.body).addClass("modal-open"),
            $(document.body).css({
                "padding-right": " 17px"
            })
        }
    });
    var embed_captcha;
    $(".reg_gt_guide-box").length > 0 && (embed_captcha = new window.Geetest({
        gt: "a5a3b6cdb1b821dd0e3033efa7ebc2e9",
        product: ""
    }).appendTo(".reg_gt_guide-box")),
    $("body").on("click", ".moder-lgn-box",
    function() {
        if (0 == $(".login-warp").length) {
            var a = $(this),
            b = "/user_action/login",
            c = {
                huxiu_hash_code: huxiu_hash_code
            };
            $.ajax({
                type: "post",
                url: b,
                data: c,
                dataType: "json",
                async: !0,
                success: function(b) {
                    "1" == b.result && ($("#login-reg-warp").append(b.data), $(".login-warp").addClass("active"), $(".login-box").addClass("overlay-dialog-animate"), $(document.body).addClass("modal-open"), $(document.body).css({
                        "padding-right": " 17px"
                    }), "reg" == a.attr("data-type") && $(".ordinary-login ul li:last-child").trigger("click"), setTimeout(function() {
                        loadScript("https://api.geetest.com/get.php",
                        function() {
                            var a;
                            a = new window.Geetest({
                                gt: "a5a3b6cdb1b821dd0e3033efa7ebc2e9",
                                product: ""
                            }).appendTo(".geetest_modal_box")
                        })
                    },
                    100))
                },
                error: function(a) {
                    Messenger().post({
                        message: c.msg,
                        type: "error",
                        showCloseButton: !0
                    })
                }
            })
        }
        $(".login-warp").hasClass("active") ? ($(".login-warp").removeClass("active"), $(".login-box").removeClass("overlay-dialog-animate"), $(document.body).removeClass("modal-open"), $(document.body).css({
            "padding-right": "0"
        })) : ($(".login-warp").addClass("active"), $(".login-box").addClass("overlay-dialog-animate"), $(document.body).addClass("modal-open"), $(document.body).css({
            "padding-right": " 17px"
        }))
    }),
    $(document).on("input propertychange", ".regphone",
    function() {
        if ("" == $(".regphone").val() || void 0 == $(".regphone").val()) $(".input-code").slideUp();
        else {
            var a = /^(((13[0-9]{1})|(15[0-9]{1})|(17[0-9]{1})|(18[0-9]{1}))+\d{8})$/;
            if (a.test($(".regphone").val())) {
                var b = ($(this), "/user/check_reg_phone"),
                c = {
                    is_ajax: "1",
                    huxiu_hash_code: huxiu_hash_code,
                    regphone: $(".regphone").val(),
                    hx_auth_token: $("#hx_auth_token").val()
                };
                $.ajax({
                    type: "post",
                    url: b,
                    data: c,
                    dataType: "json",
                    async: !0,
                    success: function(a) {
                        "1" == a.result ? ($(".regphone").addClass("success"), $(".input-code").slideDown(), Messenger().post({
                            message: a.msg,
                            type: "success",
                            showCloseButton: !0
                        }), $(".js-ver-code").attr("disabled", !1)) : Messenger().post({
                            message: a.msg,
                            type: "error",
                            showCloseButton: !0
                        })
                    },
                    error: function(a) {
                        Messenger().post({
                            message: c.msg,
                            type: "error",
                            showCloseButton: !0
                        })
                    }
                })
            } else $(".input-code").slideUp()
        }
        $(".regphone").removeClass("success"),
        $(".error-msg").html("").addClass("hide")
    }),
    $("body").on("blur", "#captchaphone",
    function() {
        var a = ($(this), "/user/check_mobile_captcha"),
        b = {
            is_ajax: 1,
            huxiu_hash_code: huxiu_hash_code,
            regphone: $(".regphone").val(),
            auth_token: $("#auth_token").val(),
            captcha: $("#captchaphone").val()
        };
        $.ajax({
            type: "post",
            url: a,
            data: b,
            dataType: "json",
            async: !0,
            success: function(a) {
                "1" == a.result && $(".js-ver-code").removeClass("has-error")
            },
            error: function(a) {
                Messenger().post({
                    message: b.msg,
                    type: "error",
                    showCloseButton: !0
                })
            }
        })
    }),
    $("body").on("blur", "#username",
    function() {
        var a = ($(this), "/user/check_reg_username"),
        b = {
            is_ajax: 1,
            huxiu_hash_code: huxiu_hash_code,
            username: $("#username").val(),
            auth_token: $("#auth_token").val(),
            captcha: $("#captchaphone").val(),
            hx_auth_token: $("#hx_auth_token").val()
        };
        $.ajax({
            type: "post",
            url: a,
            data: b,
            dataType: "json",
            async: !0,
            success: function(a) {
                "1" == a.result ? Messenger().post({
                    message: "昵称" + a.msg,
                    type: "success",
                    showCloseButton: !0
                }) : Messenger().post({
                    message: "昵称" + a.msg,
                    type: "error",
                    showCloseButton: !0
                })
            },
            error: function(a) {
                Messenger().post({
                    message: b.msg,
                    type: "error",
                    showCloseButton: !0
                })
            }
        })
    });
    var delayTime = 60;
    if ($("body").on("click", ".js-ver-code",
    function() {
        var a = $(this),
        b = "/user/send_mobile_captcha",
        c = {
            is_ajax: 1,
            huxiu_hash_code: huxiu_hash_code,
            regphone: $(".regphone").val(),
            auth_token: $("#auth_token").val(),
            geetest_challenge: $(".geetest_challenge").val(),
            geetest_validate: $(".geetest_validate").val(),
            geetest_seccode: $(".geetest_seccode").val()
        };
        return a.attr("data-type") && "back-pwd" == a.attr("data-type") && (b = "/user/send_email_captcha", c.authkey = $("#authkey").val()),
        "" != a.attr("data-type") && void 0 != a.attr("data-type") || "" != $(".geetest_challenge").val() ? void(a.hasClass("disabled") || (delayTime = 60, delayOpen(), $.ajax({
            type: "post",
            url: b,
            data: c,
            dataType: "json",
            async: !0,
            success: function(b) {
                "1" == b.result ? (Messenger().post({
                    message: b.msg,
                    type: "success",
                    showCloseButton: !0
                }), "back-pwd" == a.attr("data-type") && $(".email-prompt").removeClass("hide")) : Messenger().post({
                    message: b.msg,
                    type: "error",
                    showCloseButton: !0
                })
            },
            error: function(a) {
                Messenger().post({
                    message: c.msg,
                    type: "error",
                    showCloseButton: !0
                })
            }
        }))) : (Messenger().post({
            message: "请滑动滑块完成验证",
            type: "error",
            showCloseButton: !0
        }), !1)
    }), $("body").on("click", ".js-register-submit",
    function() {
        $(".error-msg").html("").addClass("hide");
        var a = ($(this), "/user/mobile_register"),
        b = {
            is_ajax: 1,
            huxiu_hash_code: huxiu_hash_code,
            regphone: $(".regphone").val(),
            captcha: $("#captchaphone").val(),
            username: $("#username").val(),
            password: $("#password").val(),
            hx_auth_token: $("#hx_auth_token").val(),
            geetest_challenge: $(".geetest_challenge").val(),
            geetest_validate: $(".geetest_validate").val(),
            geetest_seccode: $(".geetest_seccode").val()
        };
        return b = $.extend(b, addTaobaoParams(b)),
        $("#step").length > 0 && (b.step = $("#step").val()),
        "" == $("#regphone").val() || null == $("#regphone").val() ? ($(".error-msg").html("请输入手机号").removeClass("hide"), !1) : /^(13[0-9]|14[0-9]|15[0-9]|17[0-9]|18[0-9])\d{8}$/i.test($(".regphone").val()) ? "" == $("#captchaphone").val() || null == $("#captchaphone").val() ? ($(".error-msg").html("请输入验证码").removeClass("hide"), !1) : "" == $("#username").val() || null == $("#username").val() ? ($(".error-msg").html("请输入昵称").removeClass("hide"), !1) : "" == $("#password").val() || null == $("#password").val() ? ($(".error-msg").html("请输入密码").removeClass("hide"), !1) : void $.ajax({
            type: "post",
            url: a,
            data: b,
            dataType: "json",
            async: !0,
            success: function(a) {
                "1" == a.result ? (showMessagePrompt(a.msg), $.myDetection.gaDetection("用户注册,注册,点击"), location.reload()) : (showMessagePrompt(a.msg, "error"), embed_captcha.refresh())
            },
            error: function(a) {
                Messenger().post({
                    message: b.msg,
                    type: "error",
                    showCloseButton: !0
                })
            }
        }) : ($(".error-msg").html("请输入正确的手机号").removeClass("hide"), !1)
    }), $("body").on("click", ".js-login-submit",
    function() {
        var a = "",
        b = {};
        $.ajax({
            type: "post",
            url: a,
            data: b,
            dataType: "json",
            async: !0,
            success: function(a) {
                "1" == a.result ? (Messenger().post({
                    message: a.msg,
                    type: "success",
                    showCloseButton: !0
                }), window.location.reload()) : Messenger().post({
                    message: a.msg,
                    type: "error",
                    showCloseButton: !0
                })
            },
            error: function(a) {
                Messenger().post({
                    message: b.msg,
                    type: "error",
                    showCloseButton: !0
                })
            }
        })
    }), $("body").on("focus", ".login input",
    function() {}), $("body").on("click", ".js-empty-history",
    function() {
        $("#history").addClass("hide"),
        $.cookie("huxiu_search_history", "", {
            expires: -1
        })
    }), $("body").on("click", ".js-qr-ds",
    function() {
        $(this).css({
            opacity: "0",
            height: "0",
            overflow: "hidden"
        }).hide().animate(300,
        function() {
            $(this).css({
                display: "none"
            })
        }),
        $(".js-qr-img").removeClass("hide"),
        $(".js-qr-img").addClass("info-true")
    }), $("body").on("click", ".js-show-hide-dp-box",
    function() {
        var a = $(this);
        "true" == a.attr("data-buttom") ? ($(".span-mark-article-pl").attr("data-show", "false"), $(".span-mark-article-pl").html("展开"), a.parents(".dp-box").find(".dl-user-list").slideDown(), a.parents(".dp-box").find(".dp-list-box").hide()) : "dl-user" == a.attr("data-type") ? (a.parent(".dp-box").find(".span-mark-article-pl").html("收起"), a.parent(".dp-box").find(".span-mark-article-pl").attr("data-show", "true"), a.parent(".dp-box").find(".dl-user-list").hide(), a.parent(".dp-box").find(".dp-list-box").slideDown()) : "false" == a.attr("data-show") ? (a.html("收起"), a.parent(".dp-box").find(".dl-user-list").hide(), a.parent(".dp-box").find(".dp-list-box").slideDown(), a.attr("data-show", "true")) : (a.html("展开"), a.parents(".dp-box").find(".dl-user-list").slideDown(), a.parents(".dp-box").find(".dp-list-box").hide(), a.attr("data-show", "false"))
    }), $(document).on("mouseenter", ".article-left-btn-group .weixin",
    function() {
        var a = $(this);
        if ($(".weixin-Qr-code").find("img").attr("src")) $.myDetection.gaDetection("第三方分享,文章页,朋友圈");
        else {
            var a = $(this),
            b = "/action/weixin_qr",
            c = {
                huxiu_hash_code: huxiu_hash_code,
                id: a.attr("data-type") ? $("#topicId").val() : aid,
                type: a.attr("data-type") ? a.attr("data-type") : "article",
                f: a.attr("data-f")
            };
            $.ajax({
                type: "post",
                url: b,
                data: c,
                dataType: "json",
                async: !0,
                beforeSend: function(a) {
                    $(".weixin-Qr-code").find("img").attr("src", "/static_2015/img/loading.gif")
                },
                success: function(b) {
                    1 == b.result && ($(".weixin-Qr-code").find("img").attr("src", b.weixin_qr), "pc-friends-article" == a.attr("data-f") ? $.myDetection.gaDetection("第三方分享,文章页,朋友圈") : "pc-topic" == a.attr("data-f") && $.myDetection.gaDetection("第三方分享,热议话题,微信分享"))
                },
                error: function(a) {}
            })
        }
        a.hasClass("disabled") || (a.addClass("disabled"), $(".weixin-Qr-code").stop().css({
            opacity: "0",
            "margin-left": "80px"
        }).show().animate({
            opacity: "1",
            "margin-left": "70px"
        },
        300)),
        a.hasClass("disabled") || (a.addClass("disabled"), app.stop().css({
            opacity: "0",
            "margin-top": "-175px"
        }).show().animate({
            opacity: "1",
            "margin-top": "-165px"
        },
        300))
    }), $(document).on("mouseleave", ".article-left-btn-group .weixin",
    function() {
        var a = $(this);
        $(".weixin-Qr-code").stop().animate({
            opacity: "0",
            "margin-left": "80px"
        },
        400,
        function() {
            $(".weixin-Qr-code").hide()
        }),
        a.removeClass("disabled")
    }), $(document).on("mouseenter", ".footer-icon-list .Qr-code-footer",
    function() {
        var a = $(this),
        b = a.find(".app-qrcode");
        a.hasClass("disabled") || (a.addClass("disabled"), b.stop().css({
            opacity: "0",
            "margin-top": "-150px"
        }).show().animate({
            opacity: "1",
            "margin-top": "-140px"
        },
        300))
    }), $(document).on("mouseleave", ".js-show-promote-qr",
    function() {
        var a = $(this),
        b = a.parents(".promote-warp").find(".qr-box");
        b.stop().animate({
            opacity: "0",
            right: "180px"
        },
        400,
        function() {
            b.hide()
        }),
        a.removeClass("disabled")
    }), $(document).on("mouseenter", ".js-show-promote-qr",
    function() {
        var a = $(this),
        b = a.parents(".promote-warp").find(".qr-box");
        a.hasClass("disabled") || (a.addClass("disabled"), b.stop().css({
            opacity: "0",
            right: "180px"
        }).show().animate({
            opacity: "1",
            right: "160px"
        },
        300))
    }), $(document).on("mouseleave", ".footer-icon-list .Qr-code-footer",
    function() {
        var a = $(this),
        b = a.find(".app-qrcode");
        b.stop().animate({
            opacity: "0",
            "margin-top": "-150px"
        },
        400,
        function() {
            b.hide()
        }),
        a.removeClass("disabled")
    }), $(document).on("mouseenter", ".js-icon-moments",
    function() {
        var a = $(this),
        b = a.parent(".qr-moments-box").find(".qr-moments"),
        a = $(this),
        c = "/action/weixin_qr",
        d = {
            huxiu_hash_code: huxiu_hash_code,
            id: a.attr("data-aid"),
            type: "article",
            f: a.attr("data-f")
        };
        $.ajax({
            type: "post",
            url: c,
            data: d,
            dataType: "json",
            async: !0,
            beforeSend: function(a) {
                b.find("img").attr("src", "/static_2015/img/loading.gif")
            },
            success: function(a) {
                1 == a.result && b.find("img").attr("src", a.weixin_qr)
            },
            error: function(a) {}
        }),
        a.hasClass("disabled") || (a.addClass("disabled"), b.stop().css({
            opacity: "0",
            "margin-top": "-175px"
        }).show().animate({
            opacity: "1",
            "margin-top": "-165px"
        },
        300)),
        "index" == a.attr("data-location") ? $.myDetection.gaDetection("第三方分享,首页,朋友圈") : "column" == a.attr("data-location") && $.myDetection.gaDetection("第三方分享,栏目页,朋友圈")
    }), $(document).on("mouseleave", ".js-icon-moments",
    function() {
        var a = $(this),
        b = a.parent(".qr-moments-box").find(".qr-moments");
        b.stop().animate({
            opacity: "0",
            "margin-top": "-175px"
        },
        400,
        function() {
            b.hide()
        }),
        a.removeClass("disabled")
    }), $(document).on("mouseenter", ".js-app-guide",
    function() {
        var a = $(this),
        b = a.find(".app-guide-box");
        a.find(".guide-prompt").hide(),
        localStorage.setItem("guide", !0),
        a.hasClass("disabled") || (a.addClass("disabled"), b.stop().css({
            opacity: "0",
            "margin-top": "15px"
        }).show().animate({
            opacity: "1",
            "margin-top": "0"
        },
        300))
    }), $(document).on("mouseleave", ".js-app-guide",
    function() {
        var a = $(this),
        b = a.find(".app-guide-box");
        b.stop().animate({
            opacity: "0",
            "margin-top": "0px"
        },
        400,
        function() {
            b.hide()
        }),
        a.removeClass("disabled")
    }), $(document).on("click", ".js-app-guide",
    function() {
        window.open("/app")
    }), $(document).on("mouseenter", ".js-app-feedback",
    function() {
        var a = $(this),
        b = a.find(".app-footer-guide");
        a.hasClass("disabled") || (a.addClass("disabled"), b.stop().css({
            opacity: "0",
            left: "-155px"
        }).show().animate({
            opacity: "1",
            left: "-140px"
        },
        300))
    }), $(document).on("mouseleave", ".js-app-feedback",
    function() {
        var a = $(this),
        b = a.find(".app-footer-guide");
        b.stop().animate({
            opacity: "0",
            left: "-155px"
        },
        400,
        function() {
            b.hide()
        }),
        a.removeClass("disabled")
    }), $("body").on("click", ".js-share-article",
    function() {
        var a, b = $(this),
        c = b.attr("aid"),
        d = b.attr("pid"),
        e = (b.attr("fid"), b.attr("topic_id"), "/action/share");
        b.hasClass("js-weibo") ? (a = "hxs_tsina", "article" == b.attr("data-location") ? $.myDetection.gaDetection("第三方分享,文章页,微博") : "index" == b.attr("data-location") ? $.myDetection.gaDetection("第三方分享,首页,微博") : "index" == b.attr("data-location") && $.myDetection.gaDetection("第三方分享,栏目页,微博")) : b.hasClass("js-qzone") ? (a = "hxs_qzone", "article" == b.attr("data-location") ? ($.myDetection.gaDetection("第三方分享,文章页,QQ空间"), ga("send", "event", "第三方分享", "文章页", "QQ空间")) : "index" == b.attr("data-location") ? ($.myDetection.gaDetection("第三方分享,首页,QQ空间"), ga("send", "event", "第三方分享", "首页", "QQ空间")) : "index" == b.attr("data-location") && $.myDetection.gaDetection("第三方分享,栏目页,QQ空间")) : b.hasClass("js-thread") && (a = "hxs_tsina", $.myDetection.gaDetection("第三方分享,群组内容页,微博")),
        window.open(e + "?huxiu_hash_code=" + huxiu_hash_code + "&aid=" + c + "&pid=" + d + "&des=" + a + "&f=" + b.attr("data-f") + "&fid=" + b.attr("fid") + "&topic_id=" + b.attr("topic_id"))
    }), $("body").on("click", ".js-search-letter-btn",
    function() {
        var a = $(this);
        $(this).toggleClass("dropup"),
        $(this).toggleClass("active"),
        "true" == a.attr("data-show-box") ? (a.attr("data-show-box", "false"), a.css({
            "border-bottom-color": "#f0f0f0"
        }), a.animate({
            height: "58px"
        },
        600), setTimeout(function() {
            $(".search-letter-box").slideUp()
        },
        100)) : ($(".search-letter-box").slideDown(), a.css({
            "border-bottom-color": "#fff"
        }), a.attr("data-show-box", "true"), a.animate({
            height: "79px"
        },
        500))
    }), $("body").on("click", ".js-add-dp-box",
    function() {
        if ($(".dp-article-box").slideUp(), $(".hu-pl-box").slideUp(), $("#saytext_reply").length > 0 && ($(".pl-box-wrap textarea").attr("id", ""), $(".pl-box-wrap textarea").attr("name", "")), "none" == $(this).parent(".pl-box-btm").find(".dp-article-box").css("display")) {
            $(this).parent(".pl-box-btm").find(".dp-article-box").slideDown();
            var a = $(this).parent(".pl-box-btm").find(".dp-article-box").find("textarea");
            a.attr("id", "saytext_reply"),
            a.attr("name", "saytext_reply")
        } else $(this).parent(".pl-box-btm").find(".dp-article-box").slideUp()
    }), $("body").on("click", ".js-hf-article-pl",
    function() {
        if ($(".dp-article-box").slideUp(), $(".hu-pl-box").slideUp(), $("#saytext_reply").length > 0 && ($(".pl-box-wrap  textarea").attr("id", ""), $(".pl-box-wrap textarea").attr("name", "")), "none" == $(this).parent(".one-pl-content").find(".hu-pl-box").css("display")) {
            $(this).parent(".one-pl-content").find(".hu-pl-box").slideDown();
            var a = $(this).parent(".one-pl-content").find(".hu-pl-box").find("textarea");
            a.attr("id", "saytext_reply"),
            a.attr("name", "saytext_reply");
            var b = $(this).parent(".one-pl-content").find(".content").find(".name").eq(0).text(),
            c = "// @" + b + " ：" + $(this).parent(".one-pl-content").find(".author-content").text();
            a.data({
                dpData: "<q>" + dpFilterRep(c) + "</q>"
            }).val("回复 @" + b + " ：")
        } else $(this).parent(".one-pl-content").find(".hu-pl-box").slideUp()
    }), $("body").on("click", ".js-search-letter-close",
    function() {
        var a = $(".search-letter-btn");
        a.attr("data-show-box", "false"),
        a.animate({
            height: "58px"
        },
        600),
        a.css({
            "border-bottom-color": "#f0f0f0"
        }),
        setTimeout(function() {
            $(".search-letter-box").slideUp(),
            a.removeClass("active")
        },
        100)
    }), $("body").on("click", ".js-sea-more",
    function() {
        $(this).hasClass("active") ? ($(".tag-content-all").slideDown(), $(".tag-content-local").hide(), $(this).html('收起<span class="caret"></span>')) : ($(".tag-content-all").hide(), $(".tag-content-local").slideDown(), $(this).html('更多<span class="caret"></span>'))
    }), $("body").on("click", ".js-show-feedback-box",
    function() {
        $(".js-modal-backdrop").show(),
        $(".feedback-box").show()
    }), $("body").on("click", ".js-feedback-close",
    function() {
        $(".js-modal-backdrop").hide(),
        $(".feedback-box").hide()
    }), $("body").on("click", ".js-feedback-submit",
    function() {
        if (0 == $("#content").val().length) return $(".will-choose-error").show(),
        $(".will-choose-error").html("请输入反馈信息"),
        !1;
        var a = $(this),
        b = "/v2_action/feedback",
        c = {
            huxiu_hash_code: huxiu_hash_code,
            content: $("#content").val(),
            contact: $("#contact").val()
        };
        a.addClass("disabled"),
        $.ajax({
            type: "post",
            url: b,
            data: c,
            dataType: "json",
            async: !0,
            beforeSend: function(b) {
                a.html("正在提交"),
                a.removeClass("js-feedback-submit")
            },
            success: function(b) {
                if (1 == b.result) {
                    $("#content").val(""),
                    $("#contact").val("");
                    var c = document.location.href;
                    c.indexOf("article") >= 0 ? $.myDetection.htmDetection("用户反馈-文章页,点击,用户反馈成功") : c.indexOf("com/1.html") >= 0 ? $.myDetection.htmDetection("用户反馈-栏目页,点击,用户反馈成功") : $.myDetection.htmDetection("用户反馈-首页,点击,用户反馈成功"),
                    Messenger().post({
                        message: b.msg,
                        type: "success",
                        showCloseButton: !0
                    }),
                    $(".js-feedback-close").trigger("click"),
                    a.removeClass("disabled")
                } else Messenger().post({
                    message: b.msg,
                    type: "error",
                    showCloseButton: !0
                }),
                a.removeClass("disabled");
                a.html("提交"),
                a.addClass("js-feedback-submit")
            },
            error: function(a) {}
        })
    }), $("body").on("click", ".js-get-mod-more-list",
    function() {
        var a = $(this),
        b = "/v2_action/article_list",
        c = {
            huxiu_hash_code: huxiu_hash_code,
            page: parseInt(a.attr("data-cur_page")) + 1,
            catid: a.attr("data-catid"),
            last_dateline: a.attr("data-last_dateline")
        };
        "23" == c.catid && (c.is_free = $("#report_is_free").val()),
        $.ajax({
            type: "post",
            url: b,
            data: c,
            dataType: "json",
            async: !0,
            beforeSend: function(b) {
                a.html("正在加载..."),
                a.removeClass("js-get-mod-more-list")
            },
            success: function(b) {
                1 == b.result ? ("23" == a.attr("data-catid") && "0" == a.attr("data-cur_page") && $(".mod-info-flow").empty(), a.attr("data-last_dateline", b.last_dateline), $(".mod-info-flow").append(b.data), a.attr("data-cur_page", parseInt(a.attr("data-cur_page")) + 1), $("#loading").remove(), $("img.lazy").lazyload({
                    placeholder: "/static_2015/img/bg.png",
                    effect: "fadeIn",
                    threshold: 1
                })) : Messenger().post({
                    message: b.msg,
                    type: "success",
                    showCloseButton: !0
                }),
                parseInt(a.attr("data-cur_page")) + 1 == b.total_page && a.remove(),
                a.html("点击加载更多"),
                a.addClass("js-get-mod-more-list")
            },
            error: function(a) {}
        })
    }), $("#saytext").length > 0 && $(".pl-form-box textarea").autoResize({
        onResize: function() {
            $(this).css({
                opacity: .8
            })
        },
        animateCallback: function() {
            $(this).css({
                opacity: 1
            })
        },
        animateDuration: 300,
        extraSpace: 30
    }), $("img.lazy").lazyload({
        placeholder: "/static_2015/img/bg.png",
        effect: "fadeIn",
        threshold: 1
    }), $("body").on("mouseover", ".article-zfb-wx-box ul li",
    function() {
        var a = "";
        $(this).find(".icon-zhifb").length > 0 ? a = $(this).find(".zfbdashang-wrap") : $(this).find(".icon-weix").length > 0 && (a = $(this).find(".wxdashang-wrap")),
        a && a.stop().css({
            opacity: "0",
            "margin-top": "-190px"
        }).show().animate({
            opacity: "1",
            "margin-top": "-180px"
        },
        300),
        isOut = !1
    }), $("body").on("mouseout", ".article-zfb-wx-box ul li",
    function() {
        var a = "";
        $(this).find(".icon-zhifb").length > 0 ? a = $(this).find(".zfbdashang-wrap") : $(this).find(".icon-weix").length > 0 && (a = $(this).find(".wxdashang-wrap")),
        a && a.stop().animate({
            opacity: "0",
            "margin-top": "-180px"
        },
        400,
        function() {
            a.hide()
        }),
        isOut = !0
    }), $("body").on("click", ".js-article-pl,.js-chuangye-pl",
    function() {
        var a = $(this),
        b = parseInt(1e5 * Math.random()),
        c = $("#saytext").val(),
        d = {
            is_ajax: "1",
            random: b,
            huxiu_hash_code: huxiu_hash_code,
            message: encodeURI(c)
        };
        if ("active" == $("#comment-type").val()) {
            var e = "/active/comment",
            f = "active";
            d.hid = $("#hid").val();
            var g = $("#hid").val();
            d = addTaobaoParams(d)
        } else if ("chuangye" == $("#comment-type").val()) {
            var e = "/chuangye/add_comments",
            f = "chuangye";
            d.com_id = $("#com_id").val()
        } else {
            var e = "/action/comment",
            f = "article";
            d.aid = aid
        }
        return "" == c || null == c ? (errorAn($(".pl-form-box")), Messenger().post({
            message: "内容不能为空",
            type: "error",
            showCloseButton: !0
        }), !1) : c.length < 8 ? (errorAn($(".pl-form-box")), Messenger().post({
            message: "客官，8个字起评，不讲价哟",
            type: "error",
            showCloseButton: !0
        }), !1) : void(a.hasClass("disabled") || (a.addClass("disabled"), $.ajax({
            type: "post",
            url: e,
            data: d,
            dataType: "json",
            async: !0,
            success: function(b) {
                if (1 == b.result) {
                    var c = b;
                    "active" == f && (c = b.data),
                    "chuangye" == f && (c.pid = c.cid, $.myDetection.htmDetection("创业板-详情页-评论,点击,点击")),
                    $("#saytext").val(""),
                    "active" == $("#comment-type").val() ? $.myDetection.htmDetection("活动详情页-评论,点击,点击") : "active" == $("#comment-type").val() || $.myDetection.gaDetection("评论相关,文章页,评论");
                    var d = $(".pl-form-author").find("img").attr("src"),
                    e = $(".pl-form-author").find(".author-name").text(),
                    h = is_vip ? '<a href="/vip" target="_blank"><i class="i-vip icon-vip"></i></a>': "",
                    i = '<div class="pl-box-wrap" data-pid="' + c.pid + '" id="g_pid' + c.pid + '"><div class="pl-box-top"><div class="dropdown pull-right"><button class="btn btn-default dropdown-toggle" type="button" id="eqwe" data-toggle="dropdown" aria-haspopup="true" aria-expanded="true"><span class="caret"></span></button><ul class="dropdown-menu" aria-labelledby="dropdownMenu1"><li class="js-delpl-btn" pid="' + c.pid + '"  cid="' + c.pid + '">删除</li></ul></div><div class="author-info"><div class="author-face"><img src="' + d + '"></div><span class="author-name"><a href="/info">' + e + "</a>" + h + '</span><span class="time">刚刚</span></div><div class="pl-content">' + c.message + '</div></div><div class="pl-box-btm"><div class="article-type pull-right"><div class="icon-like-prompt"><i class="icon icon-like active"></i><span class="c1">+1</span></div><div class="icon-no-like-prompt"><i class="icon icon-no-like active"></i><span class="c1">+1</span></div><ul><li class="js-icon-like"><i class="icon icon-like "></i><span class="like">0</span></li><li class="js-no-icon-like"><i class="icon icon-no-like "></i><span>0</span></li></ul></div><div class="btn-dp transition js-add-dp-box"><i class="icon icon-dp"></i>我要点评</div><div class="pl-form-box dp-article-box"><textarea class="form-control" placeholder="客官，8个字起评，不讲价哟"></textarea><button class="btn btn-article js-article-dp">发表</button></div></div></div>';
                    $(".pl-list-wrap").length > 0 ? $(".pl-list-wrap").find("a").eq(1).after(i) : "active" == $("#comment-type").val() ? $(".pl-wrap").after('<div class="pl-list-wrap"><a href="/article/' + aid + '/1.html#pl-wrap" class="span-mark-author active">默认评论</a><a href="/article/' + aid + '/1.html?odby=dateline#pl-wrap" class="span-mark-author new ">最新评论</a>' + i + "</div>") : $(".pl-wrap").after('<div class="pl-list-wrap"><a href="/active/' + g + '/1.html#pl-wrap" class="span-mark-author active">默认评论</a><a href="/active/' + g + '/1.html?odby=dateline#pl-wrap" class="span-mark-author new ">最新评论</a>' + i + "</div>"),
                    boxAnSuccess($(".pl-form-box"), $(".pl-article-wrap"), b.message),
                    Messenger().post({
                        message: b.msg,
                        type: "success",
                        showCloseButton: !0
                    })
                } else Messenger().post({
                    message: b.msg,
                    type: "error",
                    showCloseButton: !0
                });
                a.removeClass("disabled")
            },
            error: function(a) {}
        })))
    }), $("body").on("click", ".js-icon-like",
    function() {
        var a = $(this);
        a.hasClass("active") ? $(".icon-like-prompt").find(".c1").html("-1") : $(".icon-like-prompt").find(".c1").html("+1");
        var b = $(this).parents(".article-type").find(".icon-like-prompt");
        b.css({
            opacity: "1"
        }).animate({
            opacity: "0",
            "margin-top": "-25px"
        },
        400,
        function() {
            b.css({
                "margin-top": "-13px"
            })
        })
    }), $("body").on("click", ".js-no-icon-like",
    function() {
        var a = $(this);
        a.hasClass("active") ? $(".icon-no-like-prompt").find(".c1").html("-1") : $(".icon-no-like-prompt").find(".c1").html("+1");
        var b = $(this).parents(".article-type").find(".icon-no-like-prompt");
        b.css({
            opacity: "1"
        }).animate({
            opacity: "0",
            "margin-top": "-27px"
        },
        400,
        function() {
            b.css({
                "margin-top": "-17px"
            })
        })
    }), $("body").on("click", ".js-icon-like,.js-no-icon-like",
    function() {
        var a = $(this),
        b = "",
        c = parseInt(1e5 * Math.random()),
        d = a.parents(".pl-box-wrap ").attr("data-pid"),
        e = {
            is_ajax: "1",
            random: c,
            huxiu_hash_code: huxiu_hash_code,
            pid: d
        };
        a.hasClass("disabled") || (a.addClass("disabled"), b = a.hasClass("active") ? "like" == a.attr("data-type") ? "/action/agree": "/action/disagree": "like" == a.attr("data-type") ? "/action/agree": "/action/disagree", "active" == $("#comment-type").val() && (b = "like" == a.attr("data-type") ? "/active/agreeComment": "/active/disagreeComment", e = addTaobaoParams(e)), "chuangye" == $("#comment-type").val() && (b = "/chuangye/user_click_agree_disagree", e.id = d, e.uid = uid, "like" == a.attr("data-type") ? e.act = "agree_comments": e.act = "disagree_comments"), $.ajax({
            type: "post",
            url: b,
            data: e,
            dataType: "json",
            async: !0,
            success: function(b) {
                a.hasClass("js-icon-like") ? $.myDetection.gaDetection("评论相关,文章页,点赞") : $.myDetection.gaDetection("评论相关,文章页,点差");
                var c = a.find(".like");
                "1" == b.result ? a.hasClass("active") ? (a.removeClass("active"), c.text(parseInt(c.text()) - 1), a.find("i").removeClass("active"), Messenger().post({
                    message: b.msg,
                    type: "success",
                    showCloseButton: !0
                })) : (c.text(parseInt(c.text()) + 1), a.addClass("active"), a.find("i").addClass("active"), Messenger().post({
                    message: b.msg,
                    type: "success",
                    showCloseButton: !0
                })) : Messenger().post({
                    message: b.msg,
                    type: "error",
                    showCloseButton: !0
                }),
                a.removeClass("disabled")
            },
            error: function(a) {}
        }))
    }), $("body").on("click", ".js-article-pl-anchor",
    function() {
        var a = ($(this), 100),
        b = ($(this).attr("data-href"), $("#pl-wrap-article").offset().top - a);
        $("html, body").animate({
            scrollTop: b
        },
        500),
        $("#saytext").focus()
    }), $("body").on("click", ".js-collection-article",
    function() {
        var a = $(this),
        b = "/member_action/get_favorite_category_all_list",
        c = {
            huxiu_hash_code: huxiu_hash_code,
            aid: aid
        };
        a.hasClass("disabled") || (a.addClass("disabled"), $.ajax({
            type: "post",
            url: b,
            data: c,
            dataType: "json",
            async: !0,
            success: function(b) {
                if ("1" == b.result) {
                    var c = "";
                    $.each(b.data,
                    function(a, b) {
                        var d = '<i class="icon icon-favor-radio pull-right hide"></i>';
                        c += '<div class="favorites-box js-choose-favorites" data-cid="' + b.cid + '">' + d + '<div class="favorites-name">' + b.name + '</div><div class="favorites-articel-number">' + b.count + "篇文章</div></div>"
                    });
                    var d, e;
                    d = "添加到收藏夹",
                    e = '<div class="favorites-warp">' + c + '</div><div class="btn btn-add-default js-btn-add-default"><i class="icon icon-group-add"></i>创建收藏夹</div><div class="add-favorites-box hide"><input placeholder="收藏夹名称（最多可输入20字）" id="favorites_name"><a class="btn btn-add-default js-add-favorites">创建</a></div><div class="edit-title-box"><div class="btn-group"><div class="btn btn-determine js-favorite-category">确定</div><div class="btn btn-cancel" data-dismiss="modal">取消</div></div></div>',
                    showBoxContent("collection-article", d, e)
                } else Messenger().post({
                    message: b.msg,
                    type: "error",
                    showCloseButton: !0
                });
                a.removeClass("disabled")
            },
            error: function(a) {}
        }))
    }), $("body").on("click", ".js-choose-favorites",
    function() {
        var a = $(this);
        a.find(".icon-favor-radio").toggleClass("hide")
    }), $("body").on("click", ".js-btn-add-default",
    function() {
        $(this).addClass("hide"),
        $(".add-favorites-box").removeClass("hide")
    }), $("body").on("click", ".js-add-favorites",
    function() {
        if ("" != $("#favorites_name").val()) {
            var a = ($(this), "/member_action/add_favorite_category"),
            b = {
                huxiu_hash_code: huxiu_hash_code,
                name: $("#favorites_name").val()
            };
            $.ajax({
                type: "post",
                url: a,
                data: b,
                dataType: "json",
                async: !0,
                success: function(a) {
                    if ("1" == a.result) {
                        var b = '<div class="favorites-box js-choose-favorites" data-cid="' + a.cid + '"><i class="icon icon-favor-radio pull-right"></i><div class="favorites-name">' + $("#favorites_name").val() + '</div><div class="favorites-articel-number">0篇文章</div></div>';
                        $(".favorites-warp").append(b),
                        $("#favorites_name").val(""),
                        $(".add-favorites-box").addClass("hide"),
                        $(".js-btn-add-default").removeClass("hide"),
                        $.myDetection.gaDetection("收藏,文章页,文章收藏-新建收藏夹")
                    } else Messenger().post({
                        message: a.msg,
                        type: "error",
                        showCloseButton: !0
                    })
                },
                error: function(a) {}
            })
        } else alert("还没有填写收藏夹名字哦~~")
    }), $("body").on("click", ".js-favorite-category",
    function() {
        var a = ($(this), "/member_action/add_favorite"),
        b = {
            huxiu_hash_code: huxiu_hash_code,
            aid: aid,
            cid: ""
        },
        c = $(".favorites-warp").find(".favorites-box");
        c.length > 0 && ($.each(c,
        function(a, d) {
            c.eq(a).find(".icon-favor-radio").hasClass("hide") || (b.cid += c.eq(a).attr("data-cid") + ",")
        }), b.cid.indexOf(",") >= 0 && (b.cid = b.cid.substring(0, b.cid.length - 1)), b.cid.length > 0 ? $.ajax({
            type: "post",
            url: a,
            data: b,
            dataType: "json",
            async: !0,
            success: function(a) {
                "1" == a.result ? ($.myDetection.gaDetection("收藏,文章页,文章收藏-收藏成功"), Messenger().post({
                    message: a.msg,
                    type: "success",
                    showCloseButton: !0
                })) : Messenger().post({
                    message: a.msg,
                    type: "error",
                    showCloseButton: !0
                }),
                $("#collection-article").modal("hide")
            },
            error: function(a) {}
        }) : Messenger().post({
            message: "请选择收藏夹",
            type: "error",
            showCloseButton: !0
        }))
    }), $("body").on("click", ".js-like-article",
    function() {
        var a = $(this),
        b = "/action/like",
        c = {
            huxiu_hash_code: huxiu_hash_code,
            aid: "like" == a.attr("data-type") ? aid: -parseInt(aid)
        };
        $.ajax({
            type: "post",
            url: b,
            data: c,
            dataType: "json",
            async: !0,
            success: function(b) {
                if ("1" == b.result) {
                    a.hasClass("active") ? $(".praise-box-add").find("span").html("-1") : $(".praise-box-add").find("span").html("+1");
                    var c = a.find(".praise-box-add");
                    c.css({
                        opacity: "1"
                    }).animate({
                        opacity: "0",
                        "margin-top": "-65px"
                    },
                    400,
                    function() {
                        c.css({
                            "margin-top": "-40px"
                        })
                    }),
                    a.hasClass("active") ? $(".praise-box").find(".num").text(parseInt($(".praise-box").find(".num").html()) - 1) : $(".praise-box").find(".num").text(parseInt($(".praise-box").find(".num").html()) + 1),
                    "like" == a.attr("data-type") ? a.attr("data-type", "dislike") : a.attr("data-type", "like"),
                    a.toggleClass("active"),
                    Messenger().post({
                        message: b.msg,
                        type: "success",
                        showCloseButton: !0
                    }),
                    $.myDetection.gaDetection("点赞,文章页,文章点赞")
                } else Messenger().post({
                    message: b.msg,
                    type: "error",
                    showCloseButton: !0
                })
            },
            error: function(a) {}
        })
    }), $("body").on("click", ".js-pl-dz, .js-pl-yl, .js-pl-zz",
    function() {
        var a = $(this),
        b = {
            is_ajax: 1,
            pid: a.parents(".pl-box-wrap").attr("data-pid"),
            actype: a.attr("actype"),
            huxiu_hash_code: huxiu_hash_code
        };
        if ("active" == $("#comment-type").val()) {
            var c = "/active/recommendComment";
            b.hid = $("#hid").val(),
            b = addTaobaoParams(b)
        } else var c = "/action/comment_recommend";
        $.ajax({
            type: "post",
            url: c,
            data: b,
            dataType: "json",
            async: !0,
            success: function(b) {
                1 == b.result ? ("del_recommend" == a.attr("actype") || "del_article_eye" == a.attr("actype") ? (a.parents(".pl-box-wrap").find(".btm-yl").remove(), a.attr("actype", a.attr("actype").slice(4, a.attr("actype").length)), a.parents(".pl-box-wrap").removeClass("active"), a.find("span").remove()) : (a.parents(".pl-box-wrap").find(".btm-yl").length > 0 ? a.parents(".pl-box-wrap").find("btm-yl").html(a.html()) : a.parents(".pl-box-wrap").prepend('<div class="btm-yl">' + a.html() + "</div>"), a.parents(".pl-box-wrap").addClass("active"), a.attr("actype", "del_" + a.attr("actype")), a.html("<span>取消</span>" + a.html())), Messenger().post({
                    message: b.msg,
                    type: "success",
                    showCloseButton: !0
                })) : Messenger().post({
                    message: b.msg,
                    type: "error",
                    showCloseButton: !0
                })
            },
            error: function(b) {
                Messenger().post({
                    message: "网络错误提交失败，请重试。",
                    type: "error",
                    showCloseButton: !0
                }),
                a.removeClass("disabled")
            }
        })
    }), $("body").on("click", ".js-pl-banned",
    function() {
        var a = $(this),
        b = "/setuser/stop_user",
        c = {
            is_ajax: "1",
            uid: a.attr("uid"),
            pid: a.parents(".pl-box-wrap").attr("data-pid"),
            type: a.attr("type"),
            huxiu_hash_code: huxiu_hash_code
        };
        $.ajax({
            type: "post",
            url: b,
            data: c,
            dataType: "json",
            async: !0,
            success: function(b) {
                1 == b.result ? ("startuser" == a.attr("type") ? (a.attr("type", "stopuser"), a.find("span").remove()) : (a.attr("type", "startuser"), a.html("<span>取消</span>" + a.html())), Messenger().post({
                    message: b.msg,
                    type: "success",
                    showCloseButton: !0
                })) : Messenger().post({
                    message: b.msg,
                    type: "error",
                    showCloseButton: !0
                })
            },
            error: function(a) {
                Messenger().post({
                    message: data.msg,
                    type: "error",
                    showCloseButton: !0
                })
            }
        })
    }), $("body").on("click", ".js-delpl-btn",
    function() {
        var a = $(this),
        b = parseInt(1e5 * Math.random()),
        c = a.attr("pid"),
        d = a.attr("cid"),
        e = "comment",
        f = {
            is_ajax: "1",
            random: b,
            huxiu_hash_code: huxiu_hash_code,
            pid: c,
            actype: e
        };
        if ("active" == $("#comment-type").val()) {
            var g = "/active/deleteComment";
            f = addTaobaoParams(f)
        } else if ("chuangye" == $("#comment-type").val()) {
            var g = "/chuangye/del_comments";
            f.id = a.attr("cid"),
            f.cid = a.attr("cid")
        } else var g = "/action/deldata";
        a.hasClass("disabled") || (a.addClass("disabled"), $.ajax({
            type: "post",
            url: g,
            data: f,
            dataType: "json",
            async: !0,
            success: function(b) {
                if ("1" == b.result) {
                    if ("chuangye" == $("#comment-type").val()) var e = $("#g_pid" + d);
                    else var e = $("#g_pid" + c);
                    e.css({
                        opacity: " 0.3"
                    }).find(".pl-box-nr").css({
                        height: "56px",
                        overflow: "hidden"
                    }),
                    e.slideUp(200,
                    function() {
                        $(this).remove()
                    }),
                    Messenger().post({
                        message: b.msg,
                        type: "success",
                        showCloseButton: !0
                    })
                } else Messenger().post({
                    message: b.msg,
                    type: "error",
                    showCloseButton: !0
                });
                a.removeClass("disabled")
            },
            error: function(a) {
                Messenger().post({
                    message: a,
                    type: "error",
                    showCloseButton: !0
                })
            }
        }))
    }), $("body").on("click", ".js-deldp-btn",
    function() {
        var a = $(this),
        b = parseInt(1e5 * Math.random()),
        c = a.attr("cid"),
        d = "recomment",
        e = {
            is_ajax: "1",
            random: b,
            huxiu_hash_code: huxiu_hash_code,
            cid: c,
            actype: d
        };
        if ("active" == $("#comment-type").val()) {
            var f = "/active/deleteRecomment";
            e = addTaobaoParams(e)
        } else var f = "/action/deldata";
        a.hasClass("disabled") || (a.addClass("disabled"), $.ajax({
            type: "post",
            url: f,
            data: e,
            dataType: "json",
            async: !0,
            success: function(b) {
                "1" == b.result ? ($(".del-pl" + a.attr("cid")).remove(), 0 == $(".dp-box").find(".dp-list-box").find(".dl-user").length && $(".dp-box").remove()) : Messenger().post({
                    message: b.msg,
                    type: "error",
                    showCloseButton: !0
                }),
                a.removeClass("disabled")
            },
            error: function(a) {
                Messenger().post({
                    message: a,
                    type: "error",
                    showCloseButton: !0
                })
            }
        }))
    }), $("body").on("click", ".js-article-dp",
    function() {
        var a = $(this),
        b = a.parents(".pl-box-wrap"),
        c = parseInt(1e5 * Math.random()),
        d = b.attr("data-pid"),
        e = a.parents(".dp-article-box"),
        f = $("#saytext_reply").val(),
        g = e.find(".dp-article-box textarea").data("dpData"),
        h = "undefined" == typeof g ? "": g,
        i = {
            is_ajax: "1",
            random: c,
            huxiu_hash_code: huxiu_hash_code,
            pid: d,
            message: encodeURI(f + h)
        };
        if ("active" == $("#comment-type").val()) {
            var j = "/active/recomment";
            i.hid = $("#hid").val(),
            i = addTaobaoParams(i)
        } else if ("chuangye" == $("#comment-type").val()) {
            var j = "/chuangye/recomment";
            i.cid = d
        } else {
            var j = "/action/recomment";
            i.aid = aid
        }
        if ("" == f || null == f) return errorAn(a.parents(".dp-article-box")),
        Messenger().post({
            message: "内容不能为空",
            type: "error",
            showCloseButton: !0
        }),
        !1;
        var k = $(this).parents(".one-pl-content").find(".content").find(".name").text();
        return f.replace("回复 @" + k + " ：", "").length < 8 ? (errorAn(a.parents(".dp-article-box")), errorAn(a.parents(".hu-pl-box")), Messenger().post({
            message: "客官，8个字起评，不讲价哟",
            type: "error",
            showCloseButton: !0
        }), !1) : void(a.hasClass("disabled") || (a.addClass("disabled"), $.ajax({
            type: "post",
            url: j,
            data: i,
            dataType: "json",
            async: !0,
            success: function(b) {
                var c = b;
                if ("active" == $("#comment-type").val() && (c = b.data), 1 == b.result) {
                    $(".pl-box-wrap textarea").val(""),
                    Messenger().post({
                        message: b.msg,
                        type: "success",
                        showCloseButton: !0
                    }),
                    "false" == a.parents(".pl-box-wrap").find(".span-mark-article-pl").attr("data-show") && a.parents(".pl-box-wrap").find(".span-mark-article-pl").trigger("click");
                    var d = $(".pl-form-author ").find("img").attr("src"),
                    e = $(".pl-form-author ").find(".author-name").text(),
                    f = is_vip ? '<a href="/vip" target="_blank"><i class="i-vip icon-vip"></i></a>': "",
                    g = is_vip ? '<span class="icon-s"><i class="i-vip icon-vip"></i></span>': "";
                    if (a.parents(".pl-box-wrap").find(".dp-box").length > 0) {
                        var h, i, j = a.parents(".pl-box-wrap").find(".dp-box"),
                        k = "";
                        k = '<li><a href="/member/' + uid + '.html" target="_blank"><img src="' + d + '"></a>' + g + "</li>",
                        h = '<div class="dl-user del-pl' + c.reppid + '"><ul><li><a href="/member/' + uid + '.html" target="_blank"><img src="' + d + '"></a></li></ul><div class="one-pl-content"><div class="pull-right time">刚刚</div><p class="content"><span class="name">' + e + "</span>" + f + '<span class="author-content">&nbsp;&nbsp;:' + c.message + '</span></p><div class="js-hf-article-pl"><span>回复</span></div><div class="dropdown"><button class="btn btn-default dropdown-toggle" type="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"><span class="caret"></span></button><ol class="dropdown-menu" aria-labelledby="dropdownMenu1"><li class="pl-kill js-deldp-btn" cid="' + c.reppid + '">删除</li></ol></div><div class="hu-pl-box"><textarea class="form-control" placeholder="客官，8个字起评，不讲价哟" id="" name=""></textarea><button class="btn btn-article js-article-dp" data-type="hf">发表</button></div></div></div>',
                        i = '<span class="span-mark-article-pl js-show-hide-dp-box" data-show="false">展开</span>',
                        j.find(".dl-user-list").find("ul").append(k),
                        j.find(".dp-list-box").prepend(h),
                        a.parents(".pl-box-wrap").find(".one-pl-content-box").remove()
                    } else {
                        var l = '<div class="dp-box del-pl' + c.reppid + '"><span class="span-mark-author">点评</span><span class="span-mark-article-pl js-show-hide-dp-box" data-show="false">展开</span><div class="dl-user dl-user-list"><ul><li class="del-pl' + c.reppid + '"><a href="/member/' + uid + '.html" target="_blank"><img src="' + d + '"></a></li></ul><div class="one-pl-content one-pl-content-box"><div class="pull-right time">刚刚</div><p class="content"><span class="name">' + e + "</span>" + f + '<span class="author-content">&nbsp;&nbsp;:' + c.message + '</span></p><div class="js-hf-article-pl"><span>回复</span></div><div class="dropdown"><button class="btn btn-default dropdown-toggle" type="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"><span class="caret"></span></button><ol class="dropdown-menu" aria-labelledby="dropdownMenu1"><li class="pl-kill js-deldp-btn" cid="' + c.reppid + '">删除</li></ol></div><div class="hu-pl-box"><textarea class="form-control" placeholder="客官，8个字起评，不讲价哟"></textarea><button class="btn btn-article js-article-dp" data-type="hf">发表</button></div></div></div><div class="dp-list-box"><div class="dl-user del-pl' + c.reppid + '"><ul><li><a href="/member/' + uid + '.html" target="_blank"><img src="' + d + '"></a></li></ul><div class="one-pl-content"><div class="pull-right time">刚刚</div><p class="content"><span class="name">' + e + "</span>" + c.message + '</p><div class="js-hf-article-pl"><span>回复</span></div><div class="dropdown"><button class="btn btn-default dropdown-toggle" type="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"><span class="caret"></span></button><ol class="dropdown-menu" aria-labelledby="dropdownMenu1"><li class="pl-kill js-deldp-btn" cid="' + c.reppid + '">删除</li></ol></div><div class="hu-pl-box"><textarea class="form-control" placeholder="客官，8个字起评，不讲价哟"></textarea><button class="btn btn-article js-article-dp" data-type="hf">发表</button></div></div></div><div class="close-dp-list-box js-show-hide-dp-box" data-buttom="true">收起</div></div></div>';
                        a.parents(".pl-box-wrap").find(".pl-box-top").append(l).slideDown()
                    }
                    $(".dp-article-box").slideUp(),
                    $(".hu-pl-box").slideUp(),
                    $("#saytext_reply").length > 0 && ($(".pl-box-wrap  textarea").attr("id", ""), $(".pl-box-wrap  textarea").attr("name", "")),
                    "hf" == a.attr("data-type") ? $.myDetection.gaDetection("评论相关,文章页,回复点评") : $.myDetection.gaDetection("评论相关,文章页,点评")
                } else Messenger().post({
                    message: b.msg,
                    type: "error",
                    showCloseButton: !0
                }); ! a.removeClass("disabled")
            },
            error: function(a) {}
        })))
    }), $(document).on("click", ".dp-box .dl-user q",
    function() {
        var a = $(this);
        a.hasClass("js-open") ? (a.removeClass("js-open"), a.css({
            display: "inline-block",
            background: "#0479c4",
            color: "#fff"
        },
        100)) : (a.addClass("js-open"), a.css({
            display: "inline",
            background: "transparent",
            color: "#555"
        },
        100))
    }), $("body").on("click", ".js-default-new-pl",
    function() {
        $(".js-get-pl-more-list").removeClass("hide");
        var a = $(this),
        b = {
            huxiu_hash_code: huxiu_hash_code,
            page: 1,
            type: a.attr("data-type")
        };
        if ("active" == $("#comment-type").val()) {
            var c = "/active/getComments";
            b.hid = $("#hid").val()
        } else if ("chuangye" == $("#comment-type").val()) {
            var c = "/chuangye/comment_list";
            b.com_id = $("#com_id").val()
        } else {
            var c = "/v2_action/comment_list";
            b.aid = aid
        }
        $(".js-default-new-pl").removeClass("active"),
        a.addClass("active"),
        $.ajax({
            type: "post",
            url: c,
            data: b,
            dataType: "json",
            async: !0,
            beforeSend: function(a) {
                $(".pl-loading").removeClass("hide")
            },
            success: function(b) {
                1 == b.result && ($(".pl-box-wrap ").remove(), $(".pl-list-wrap").append(b.data), $(".js-get-pl-more-list").attr("data-cur_page", 300), $(".js-get-pl-more-list").attr("data-type", a.attr("data-type"))),
                b.cur_page == b.total_page && $(".js-get-pl-more-list").addClass("hide"),
                $(".pl-loading").addClass("hide")
            },
            error: function(a) {}
        })
    }), $("body").on("click", ".js-get-pl-more-list",
    function() {
        var a = $(this),
        b = {
            huxiu_hash_code: huxiu_hash_code,
            page: parseInt(a.attr("data-cur_page")) + 1,
            type: a.attr("data-type")
        };
        if ("active" == $("#comment-type").val()) {
            var c = "/active/getComments";
            b.hid = $("#hid").val()
        } else {
            var c = "/v2_action/comment_list";
            b.aid = aid
        }
        return a.hasClass("disabled") ? (Messenger().post({
            message: "没有更多评论了。",
            type: "error",
            showCloseButton: !0
        }), !1) : void $.ajax({
            type: "post",
            url: c,
            data: b,
            dataType: "json",
            async: !0,
            success: function(b) {
                1 == b.result && ("" == b.data && Messenger().post({
                    message: "没有更多评论了。",
                    type: "error",
                    showCloseButton: !0
                }), $(".pl-list-wrap").append(b.data), a.attr("data-cur_page", parseInt(a.attr("data-cur_page")) + 1)),
                b.cur_page == b.total_page && a.addClass("hide")
            },
            error: function(a) {}
        })
    }), $("body").on("click", ".js-report-pl,.js-report-dp,.js-group-report",
    function() {
        var a = $(this),
        b = "";
        if (a.hasClass("js-report-pl")) var c = a.attr("pid"),
        d = "js-rep-pl-btn";
        else if (a.hasClass("js-report-dp")) var c = a.attr("reppid"),
        d = "js-rep-dp-btn";
        else if (a.hasClass("js-group-report")) {
            var c = a.attr("reppid"),
            b = a.attr("data-type");
            d = "js-group-report-btn"
        }
        if (!a.hasClass("disabled")) {
            a.addClass("disabled");
            var e = a.attr("aid"),
            f = '<div class="rep-wrap"><div class="form-horizontal rep-moder-box" type="' + b + '" aid="' + e + '" reportid="' + c + '"><label class="radio-inline"><i class="icon icon-radio"></i><input type="radio" name="repRadio" id="repRadio1" value="色情"> 色情</label><label class="radio-inline"><i class="icon icon-radio"></i><input type="radio" name="repRadio" id="repRadio2" value="谣言"> 谣言</label><label class="radio-inline"><i class="icon icon-radio"></i><input type="radio" name="repRadio" id="repRadio3" value="网络钓鱼/广告">网络钓鱼/广告</label><label class="radio-inline"><i class="icon icon-radio"></i><input type="radio" name="repRadio" id="repRadio4" value="政治"> 政治</label><label class="radio-inline"><i class="icon icon-radio"></i><input type="radio" name="repRadio" id="repRadio5" value="侵权"> 侵权</label><label class="radio-inline"><i class="icon icon-radio"></i><input type="radio" name="repRadio" id="repRadio6" value="人身攻击"> 人身攻击</label><h4 class="t-h4">补充说明</h4><div class="textarea-box"><textarea class="form-control" rows="3"></textarea></div></div></div>',
            g = '<div class="clearfix text-right rep-moder-btm"><button class="btn btn-blue ' + d + '">提交</button></div>';
            showBox("jb_model", "举报", f, g),
            a.removeClass("disabled")
        }
    }), $("body").on("click", ".js-rep-pl-btn,.js-rep-dp-btn",
    function() {
        var a = $(this);
        if (a.hasClass("js-rep-pl-btn")) var b = "comment";
        else if (a.hasClass("js-rep-dp-btn")) var b = "dianping";
        var c = $(".rep-moder-box"),
        d = parseInt(1e5 * Math.random()),
        e = "/setuser/report",
        f = c.attr("reportid"),
        g = c.attr("aid"),
        h = c.find("input:checked").val(),
        i = c.find(".textarea-box textarea").val(),
        j = {
            is_ajax: "1",
            random: d,
            huxiu_hash_code: huxiu_hash_code,
            reportid: f,
            aid: g,
            type: b,
            description: encodeURI("#" + h + "#" + i)
        };
        return "undefined" == typeof h ? (Messenger().post({
            message: "请选择一个举报类型",
            type: "error",
            showCloseButton: !0
        }), !1) : void(a.hasClass("disabled") || (a.addClass("disabled"), $.ajax({
            type: "post",
            url: e,
            data: j,
            dataType: "json",
            async: !0,
            success: function(b) {
                if ("1" == b.result) {
                    if (a.hasClass("js-rep-pl-btn")) {
                        var c = $("#g_pid" + f);
                        c.find(".pl-box").css({
                            background: "#fcb8b8"
                        })
                    } else if (a.hasClass("js-rep-dp-btn")) {
                        var c = $(".dianping-box[reppid=" + f + "]");
                        c.css({
                            opacity: ".6"
                        })
                    }
                    Messenger().post({
                        message: b.msg,
                        type: "success",
                        showCloseButton: !0
                    })
                } else Messenger().post({
                    message: b.msg,
                    type: "error",
                    showCloseButton: !0
                });
                a.removeClass("disabled")
            },
            error: function(b) {
                Messenger().post({
                    message: "网络错误提交失败，请重试。",
                    type: "error",
                    showCloseButton: !0
                }),
                a.removeClass("disabled")
            }
        })))
    }), $("body").on("click", ".js-get-tag-more-list",
    function() {
        var a = $(this),
        b = "/v2_action/tag_article_list",
        c = {
            huxiu_hash_code: huxiu_hash_code,
            page: a.attr("data-cur_page"),
            tag_id: a.attr("data-tag_id")
        };
        a.hasClass("disabled") ? Messenger().post({
            message: "没有更多标签了",
            type: "error",
            showCloseButton: !0
        }) : $.ajax({
            type: "post",
            url: b,
            data: c,
            dataType: "json",
            async: !0,
            beforeSend: function(b) {
                a.html("正在加载..."),
                a.removeClass("js-get-tag-more-list")
            },
            success: function(b) {
                if (1 == b.result) {
                    var c = "";
                    $.each(b.data,
                    function(a, b) {
                        c += '<li><a href="' + b.url + '" target="_blank">' + b.title + '</a><span class="pull-right time">' + b.time + "</span></li>"
                    }),
                    a.attr("data-cur_page", parseInt(a.attr("data-cur_page")) + 1),
                    $(".related-article ul").append(c),
                    parseInt(a.attr("data-cur_page")) - 1 == b.total_page && (a.addClass("disabled"), a.remove())
                } else Messenger().post({
                    message: b.msg,
                    type: "error",
                    showCloseButton: !0
                });
                a.addClass("js-get-tag-more-list"),
                a.html("点击加载更多")
            },
            error: function(a) {}
        })
    }), $(".js-pc-del").length > 0 && $(".js-pc-del").click(function() {
        btn = $(this);
        var a = "del_article_top",
        b = "删除",
        c = "确认要删除吗？",
        d = '<div><button class="btn js-pc-del-article" data-dismiss="modal">删除</button><button type="button" class="btn btn-gray" data-dismiss="modal">取消</button></div>';
        showBox(a, b, c, d)
    }), $("body").on("click", ".js-btn-related",
    function() {
        var a = "get";
        getRelatedInfo(showBox, a, "", $(this))
    }), $("body").on("click", ".js-submit",
    function() {
        var a = "add",
        b = $(".js-text").val();
        getRelatedInfo(showBox, a, b, $(this))
    }), $("body").on("click", ".js-remove",
    function() {
        var a = "del",
        b = $(this).parents("li").find(".url").html();
        getRelatedInfo(showBox, a, b, $(this))
    }), $("body").on("click", ".js-btn-ignored",
    function() {
        getIgnoredList($(this))
    }), $("body").on("click", "#ignoreModal .article-check-ignore-conform",
    function() {
        var btn = $(this),
        oParent = btn.parents(".modal"),
        oReasonBox = oParent.find(".js-reason-box"),
        iReason = oReasonBox.find(".js-custom-reason").val(),
        aid = $(this).attr("aid"),
        url = "/admin/article_ignore_action",
        param = {
            huxiu_hash_code: huxiu_hash_code,
            aid: aid
        },
        reason = new Array,
        i = 0;
        if (!btn.hasClass("disabled")) {
            if ($.each(oReasonBox.find('.new-lb input[type="checkbox"]'),
            function(a, b) {
                var c = $(b).val(),
                d = $(b).attr("id"),
                e = 1 == $(b).prop("checked") ? !0 : !1;
                e && (reason[i] = {
                    id: d,
                    message: c
                },
                i++)
            }), "" != iReason && (reason[reason.length] = {
                id: 0,
                message: iReason
            }), !reason[0] && "" == iReason && 0 == $("#is-group-message").prop("checked")) return void alert("请至少选择一种忽略理由");
            param.reasons = reason,
            param.ismessage = 1 == $("#is-group-message").prop("checked") ? 1 : 0,
            $.post(url, param,
            function(data) {
                var data = eval("(" + data + ")");
                1 == data.result ? ($("#ignoreModal").modal("hide"), window.location.reload()) : ($(".js-alert").addClass("alert alert-danger").removeClass("alert-success").html("忽略理由修改失败"), setTimeout(function() {
                    $(".js-alert").removeClass("alert alert-danger").html("")
                },
                1500)),
                btn.removeClass("disabled")
            })
        }
    }), $("body").on("click", "#ignoreModal .js-modal-manage",
    function() {
        var a = $(this),
        b = a.parents(".modal"),
        c = b.find(".js-reason-box"),
        d = b.find(".js-reason-edit-box");
        $.each(c.find('.new-lb input[type="checkbox"]'),
        function(a, b) {
            var c = '<label class="new-lb"><span class="remove-article-reason">-</span><input class="form-control" id="' + $(b).attr("id") + '" name="reason" type="text" value="' + $(b).val() + '" /></label>';
            d.append(c)
        }),
        c.css("display", "none"),
        a.attr("class", "js-btn-reason-add").html("添加"),
        b.find(".article-check-ignore-conform").attr("class", "btn btn-success js-btn-article-manage-ignore")
    }), $("body").on("click", "#ignoreModal .js-reason-edit-box .new-lb span",
    function() {
        var btn = $(this),
        iReasonBox = btn.parent().find('input[type="text"]'),
        url = "/admin/article_reason_delete_action",
        param = {
            huxiu_hash_code: huxiu_hash_code,
            reason_id: iReasonBox.attr("id")
        };
        return void 0 == iReasonBox.attr("id") ? void iReasonBox.parent().remove() : void $.post(url, param,
        function(data) {
            data = eval("(" + data + ")"),
            1 == data.result ? btn.parent().remove() : ($(".js-alert").addClass("alert alert-danger").removeClass("alert-success").html("忽略理由修改失败"), setTimeout(function() {
                $(".js-alert").removeClass("alert alert-danger").html("")
            },
            1500))
        })
    }), $("body").on("click", ".js-btn-reason-add",
    function() {
        var a = $(this),
        b = a.parents(".modal"),
        c = b.find(".js-reason-edit-box");
        c.prepend('<label class="new-lb"><span class="remove-article-reason">-</span><input class="form-control" name="reason" type="text" value="" /></label>'),
        c.find(".new-lb:first-child input").focus()
    }), $("body").on("click", ".js-btn-article-manage-ignore",
    function() {
        var btn = $(this),
        oParent = btn.parents(".modal"),
        oReasonEditBox = oParent.find(".js-reason-edit-box"),
        urlModify = "/admin/article_reason_edit_action",
        urlAdd = "/admin/article_reason_add_action",
        paramAdd = {
            huxiu_hash_code: huxiu_hash_code
        },
        paramModify = {
            huxiu_hash_code: huxiu_hash_code
        },
        arrModify = [],
        arrAdd = [];
        btn.hasClass("disabled") || (btn.addClass("disabled"), $.each(oReasonEditBox.find('.new-lb input[type="text"]'),
        function(a, b) {
            if (void 0 == $(b).attr("id")) arrAdd.push($(b).val());
            else {
                var c = {};
                c.id = $(b).attr("id"),
                c.message = $(b).val(),
                arrModify.push(c)
            }
            paramAdd.reason = arrAdd,
            paramModify.reason = arrModify
        }), arrAdd.length > 0 && $.post(urlAdd, paramAdd,
        function(data) {
            var data = eval("(" + data + ")");
            1 == data.result ? $("#ignoreModal").modal("hide") : ($(".js-alert").addClass("alert alert-danger").removeClass("alert-success").html("忽略理由修改失败"), setTimeout(function() {
                $(".js-alert").removeClass("alert alert-danger").html("")
            },
            1500)),
            btn.removeClass("disabled")
        }), arrModify.length > 0 && $.post(urlModify, paramModify,
        function(data) {
            var data = eval("(" + data + ")");
            1 == data.result ? $("#ignoreModal").modal("hide") : ($(".js-alert").addClass("alert alert-danger").removeClass("alert-success").html("忽略理由修改失败"), setTimeout(function() {
                $(".js-alert").removeClass("alert alert-danger").html("")
            },
            1500)),
            btn.removeClass("disabled")
        }))
    }), $("body").on("mouseover", ".zhifb-mouseover",
    function() {
        if ($(this).find(".icon-zhifb").length > 0) {
            var a = "文章打赏_支付宝,作家名称," + aid;
            $.myDetection.htmDetection(a)
        }
    }), $("body").on("mouseover", ".weix-mouseover",
    function() {
        if ($(this).find(".icon-weix").length > 0) {
            var a = "文章打赏_微信,作家名称," + aid;
            $.myDetection.htmDetection(a)
        }
    }), $("body").on("click", ".js-push-model",
    function() {
        var a = $(this);
        if ("main" == a.attr("data-location")) {
            var b = "/v2_admin_action/push_article_get",
            c = {
                is_ajax: 1,
                huxiu_hash_code: huxiu_hash_code,
                aid: aid
            };
            $.ajax({
                type: "post",
                url: b,
                data: c,
                dataType: "json",
                async: !0,
                success: function(b) {
                    var c = "",
                    d = "",
                    e = 0;
                    1 == b.result ? ($.each(b.list,
                    function(b, f) {
                        1 == f.pushed ? (c += '<label class="btn" title="' + f.name + '" push_type="' + f.push_type + '" for="itemid' + f.push_type + '" disabled><input  id="itemid' + f.push_type + '" name="item" type="radio" disabled>' + f.name + "</label>", e += 1, d += '<span class="btn active" push_type="' + f.push_type + '" aid="' + a.attr("aid") + '" title="' + f.name + '"><i></i><input type="checkbox" checked="checked">' + f.name + "</span>") : c += '<label class="btn" title="' + f.name + '" push_type="' + f.push_type + '" for="itemid' + f.push_type + '" ><input  id="itemid' + f.push_type + '" name="item" type="radio">' + f.name + "</label>"
                    }), c = '<div class="btn-group checkbox-list modal-push-box" data-toggle="buttons">' + c + "</div>", d = e > 0 ? '<br/><br/><div class="alert alert-success push-modal-title">已推送到下列位置</div><div class="btn-group checkbox-list modal-push-box new-manage-push-btn-wrap" data-toggle="buttons">' + d + "</div>": '<br/><br/><hr style="margin:10px 0;"><div class="text-center"><span class="label" style="padding:5px 10px;">这篇文章还没有被推送过</span></div>') : c = '<div class="alert alert-error">' + b.msg + "</div>";
                    var f = '<div class="modal-body"><div class="alert alert-success push-modal-title">推送列表：</div>' + c + d + "</div>",
                    g = '<button class="btn btn-success new-push-modal2" aid="' + a.attr("aid") + '" data-dismiss="modal" aria-hidden="true">确定</button><button class="btn" data-dismiss="modal" aria-hidden="true">取消</button>';
                    showBox("newPushModal", "新版管理推送", f, g)
                },
                error: function(a) {
                    Messenger().post({
                        message: data.msg,
                        type: "error",
                        showCloseButton: !0
                    })
                }
            })
        }
    }), $("body").on("click", ".new-push-modal2",
    function() {
        var a = $(this),
        b = "/v2_admin_action/push_article_add",
        c = {
            huxiu_hash_code: huxiu_hash_code,
            aid: a.attr("aid"),
            push_type: $(".modal-push-box").eq(0).find('.btn input[type="radio"]:checked').parent().attr("push_type")
        };
        return void 0 == c.push_type ? (Messenger().post({
            message: "请选择推送位置。",
            type: "error",
            showCloseButton: !0
        }), !1) : void $.ajax({
            type: "post",
            url: b,
            data: c,
            dataType: "json",
            async: !0,
            success: function(a) {
                1 == a.result ? Messenger().post({
                    message: a.msg,
                    type: "success",
                    showCloseButton: !0
                }) : Messenger().post({
                    message: a.msg,
                    type: "error",
                    showCloseButton: !0
                })
            },
            error: function(a) {
                Messenger().post({
                    message: a.msg,
                    type: "error",
                    showCloseButton: !0
                })
            }
        })
    }), $("body").on("click", ".new-manage-push-btn-wrap .btn",
    function() {
        if (confirm("确认要取消推送么？")) {
            var a = $(this),
            b = "/v2_admin_action/push_article_delete",
            c = {
                huxiu_hash_code: huxiu_hash_code,
                aid: a.attr("aid"),
                push_type: a.attr("push_type")
            };
            $.ajax({
                type: "post",
                url: b,
                data: c,
                dataType: "json",
                async: !0,
                success: function(b) {
                    if (1 == b.result) {
                        Messenger().post({
                            message: b.msg,
                            type: "success",
                            showCloseButton: !0
                        }),
                        a.remove();
                        var c = $(".modal-push-box").find("label");
                        $.each(c,
                        function(b, d) {
                            c.eq(b).attr("push_type") == a.attr("push_type") && (c.eq(b).removeAttr("disabled"), c.eq(b).find("input").removeAttr("disabled"))
                        })
                    } else Messenger().post({
                        message: b.msg,
                        type: "error",
                        showCloseButton: !0
                    })
                },
                error: function(a) {
                    Messenger().post({
                        message: a.msg,
                        type: "error",
                        showCloseButton: !0
                    })
                }
            })
        }
    }), $("body").on("click", ".js-pc-del-article",
    function() {
        var a = ($(this), "/action/deldata"),
        b = {
            huxiu_hash_code: huxiu_hash_code,
            is_ajax: 1,
            actype: "article",
            aid: aid
        };
        $.ajax({
            type: "post",
            url: a,
            data: b,
            dataType: "json",
            async: !0,
            success: function(a) {
                1 == a.result ? Messenger().post({
                    message: a.msg,
                    type: "success",
                    showCloseButton: !0
                }) : Messenger().post({
                    message: a.msg,
                    type: "error",
                    showCloseButton: !0
                })
            },
            error: function(a) {
                Messenger().post({
                    message: a.msg,
                    type: "error",
                    showCloseButton: !0
                })
            }
        })
    }), $("body").on("click", ".js-push-outs",
    function() {
        var a = ($(this), "/pushdata"),
        b = {
            huxiu_hash_code: huxiu_hash_code,
            aid: aid,
            ftype: "pushAd",
            is_ajax: 1,
            act: "getList"
        };
        $.ajax({
            type: "post",
            url: a,
            data: b,
            dataType: "json",
            async: !0,
            success: function(a) {
                if (1 == a.result) {
                    var b = "";
                    $.each(a.content,
                    function(a, c) {
                        var d = "";
                        1 == c.status && (d = "checked"),
                        b += '<label class="checkbox-inline"><input name="pro[]" oid="' + c.oid + '" openid="' + c.openid + '" ' + d + ' type="checkbox" >' + c.openname + "</label>"
                    });
                    var c = "push_box_three_party",
                    d = "管理第三方推送",
                    e = '<div class="js-msg"></div><div class="">' + b + "</div>",
                    f = '<button type="button" class="btn btn-success js-btn-push-three">提交</button> <button type="button" class="btn btn-gray" data-dismiss="modal">关闭</button>';
                    showBox(c, d, e, f)
                } else Messenger().post({
                    message: a.msg,
                    type: "error",
                    showCloseButton: !0
                })
            },
            error: function(a) {
                Messenger().post({
                    message: a,
                    type: "error",
                    showCloseButton: !0
                })
            }
        })
    }), $("body").on("click", ".js-btn-shensu",
    function() {
        var a = "d_shensu_box",
        b = '<div class="js-alert"></div><div><p>您可以再次<a href="/contribute?aid=' + $(this).attr("aid") + '">编辑</a>您的稿件，然后在这里写下您的申诉理由。我们会对您的稿件进行复核。复核为终审，如果您的稿件还是没有通过，我们只能表示非常遗憾。</p><textarea class="form-control js-text" placeholder="您可在此输入申诉理由" rows="5"></textarea></div>',
        c = "填写申诉理由",
        d = '<button class="btn btn-success js-btn-submit" aid="' + $(this).attr("aid") + '">确定</button>';
        showBox(a, c, b, d)
    }), $("body").on("click", "#d_shensu_box .js-btn-submit",
    function() {
        var btn = $(this);
        if (!btn.hasClass("disabled")) {
            btn.addClass("disabled");
            var url = "/setuser/author_reason",
            param = {
                huxiu_hash_code: huxiu_hash_code,
                is_ajax: 1,
                aid: aid,
                message: $("#d_shensu_box .js-text").val()
            };
            $.each($(".js-radio-box input"),
            function(a, b) {
                return 1 == $(b).prop("checked") ? void(param.clickid = $(b).val()) : void 0
            }),
            $.post(url, param,
            function(data) {
                data = eval("(" + data + ")"),
                1 == data.result ? (btn.removeClass("disabled"), $(".js-alert").addClass("alert alert-success").removeClass("alert-danger").html("申诉成功"), setTimeout(function() {
                    $(".js-alert").removeClass("alert alert-success").html(""),
                    location.reload()
                },
                1500)) : ($(".js-alert").addClass("alert alert-danger").removeClass("alert-success").html(data.msg), setTimeout(function() {
                    $(".js-alert").removeClass("alert alert-danger").html("")
                },
                1500)),
                btn.removeClass("disabled")
            })
        }
    }), $("body").on("click", ".js-btn-push-three",
    function() {
        var a = ($(this), []);
        $.each($(".modal-body").find(".checkbox-inline"),
        function(b, c) {
            var d = $(c).find("input:checked").attr("openid");
            a[b] = d
        });
        var b = "/pushdata",
        c = {
            huxiu_hash_code: huxiu_hash_code,
            aid: aid,
            act: "getSubmit",
            pro: a,
            ftype: "pushAd"
        };
        $.ajax({
            type: "post",
            url: b,
            data: c,
            dataType: "json",
            async: !0,
            success: function(a) {
                1 == a.result ? (Messenger().post({
                    message: a.msg,
                    type: "success",
                    showCloseButton: !0
                }), setTimeout(function() {
                    location.reload()
                },
                2e3)) : Messenger().post({
                    message: a.msg,
                    type: "error",
                    showCloseButton: !0
                })
            },
            error: function(a) {
                Messenger().post({
                    message: a,
                    type: "error",
                    showCloseButton: !0
                })
            }
        })
    }), $("body").on("click", ".js-push-topic",
    function() {
        var a = ($(this), "/pushdata"),
        b = {
            huxiu_hash_code: huxiu_hash_code,
            aid: aid,
            act: "getList",
            ftype: "pushZt"
        };
        $.ajax({
            type: "post",
            url: a,
            data: b,
            dataType: "json",
            async: !0,
            success: function(a) {
                if (1 == a.result) {
                    var b = '<li class="js-type-opt" ztnameen="default" zid="0">默认无选择</li>',
                    c = "<li>还未选择专题</li>";
                    $.each(a.content,
                    function(a, c) {
                        b += '<li class="js-type-opt" ztnameen="' + c.ztnameen + '" zid="' + c.zid + '">' + c.zanzhushang + "</li>"
                    });
                    var d = "push_box_zt",
                    e = "管理专题推送",
                    f = '<div class="js-msg"></div><div class="clearfix"><ul class="form-control js-zt-type">' + b + '</ul><ul class="form-control js-zt-type-cnt">' + c + "</ul></div>",
                    g = '<button type="button" class="btn btn-success js-btn-push-zt">提交</button> <button type="button" class="btn btn-gray" data-dismiss="modal">关闭</button>';
                    showBox(d, e, f, g)
                } else Messenger().post({
                    message: a.msg,
                    type: "error",
                    showCloseButton: !0
                })
            },
            error: function(a) {
                Messenger().post({
                    message: a,
                    type: "error",
                    showCloseButton: !0
                })
            }
        })
    }), $("body").on("click", ".js-zt-type .js-type-opt, .js-zt-type-cnt .js-type-opt",
    function() {
        $(this).parent().find("li").removeClass("active"),
        $(this).addClass("active")
    }), $(document).on("click", ".js-zt-type .js-type-opt",
    function() {
        var a = $(this).attr("zid");
        if (0 == a) $(".js-zt-type-cnt").html("<li>还未选择专题</li>");
        else {
            var b = "/pushdata",
            c = {
                huxiu_hash_code: huxiu_hash_code,
                aid: aid,
                act: "getClass",
                ftype: "pushZt",
                zid: a
            };
            $.ajax({
                type: "post",
                url: b,
                data: c,
                dataType: "json",
                async: !0,
                success: function(a) {
                    if (1 == a.result) {
                        var b = "";
                        $.each(a.content,
                        function(a, c) {
                            b += '<li class="js-type-opt" tid="' + c.tid + '">' + c.ztclassname + "</li>"
                        }),
                        $(".js-zt-type-cnt").html(b)
                    } else $(".js-msg").addClass("alert alert-danger").removeClass("hidden").html(a.msg),
                    setTimeout(function() {
                        $(".js-msg").removeClass("alert alert-danger").html("")
                    },
                    2e3)
                },
                error: function(a) {
                    Messenger().post({
                        message: a,
                        type: "error",
                        showCloseButton: !0
                    })
                }
            })
        }
    }), $("body").on("click", ".js-btn-push-zt",
    function() {
        var a = $(".js-zt-type-cnt").find("li.active").attr("tid"),
        b = $(".js-zt-type").find("li.active").attr("ztnameen"),
        c = $(".js-zt-type").find("li.active").attr("zid");
        if ($(".js-zt-type-cnt li").length > 1) {
            void 0 == a && (a = $(".js-zt-type-cnt li").eq(1).attr("tid"));
            var d = {
                huxiu_hash_code: huxiu_hash_code,
                aid: aid,
                act: "getSubmit",
                ftype: "pushZt",
                zid: c,
                tid: a,
                ztnameen: b
            }
        } else if (0 == $(".js-zt-type").find("li.active").length) $(".js-msg").addClass("alert alert-danger").html("您还没有选择"),
        setTimeout(function() {
            $(".js-msg").removeClass("alert alert-danger").html("")
        },
        2e3);
        else if (0 == c) var d = {
            huxiu_hash_code: huxiu_hash_code,
            aid: aid,
            act: "getSubmit",
            ftype: "pushZt"
        };
        var e = "/pushdata";
        $.ajax({
            type: "post",
            url: e,
            data: d,
            dataType: "json",
            async: !0,
            success: function(a) {
                1 == a.result ? (Messenger().post({
                    message: a.msg,
                    type: "success",
                    showCloseButton: !0
                }), setTimeout(function() {
                    location.reload()
                },
                2e3)) : Messenger().post({
                    message: a.msg,
                    type: "error",
                    showCloseButton: !0
                })
            },
            error: function(a) {
                Messenger().post({
                    message: a,
                    type: "error",
                    showCloseButton: !0
                })
            }
        })
    }), $("body").on("click", ".js-btn-resend",
    function() {
        var a = $(this),
        b = {
            is_ajax: "1",
            huxiu_hash_code: huxiu_hash_code,
            regtype: a.attr("type"),
            email: a.attr("email"),
            auth_token: $("#auth_token").val()
        };
        $.ajax({
            type: "post",
            url: "/user/hx_send_email",
            data: b,
            dataType: "json",
            async: !0,
            success: function(a) {
                1 == a.result ? Messenger().post({
                    message: a.msg,
                    type: "success",
                    showCloseButton: !0
                }) : Messenger().post({
                    message: a.msg,
                    type: "error",
                    showCloseButton: !0
                })
            },
            error: function(a) {
                Messenger().post({
                    message: a,
                    type: "error",
                    showCloseButton: !0
                })
            }
        })
    }), $("#page_404").length > 0 && delayURL(), $(".js-yarcrontab").length > 0 && $.get("https://www.huxiu.com/yarcrontab.html",
    function(a) {}), $("#container").length > 0 && $("#container").css("height", "0"), 0 == uid && -1 == window.location.href.indexOf("/user/login")) {
        var url = window.location.href.replace("http://" + window.location.host, "");
        localStorage.setItem("callback_url", url)
    }
    0 != uid && $.ajax({
        type: "post",
        url: "/member_action/get_message_count",
        data: {
            huxiu_hash_code: huxiu_hash_code
        },
        dataType: "json",
        async: !0,
        success: function(a) {
            if (1 == a.result) {
                var b = a.data.comment_message_num,
                c = a.data.system_message_num,
                d = a.data.private_message_num;
                b + c + d && $(".message-num").show(),
                $(".comment_message").html(b ? b: ""),
                $(".system_message").html(c ? c: ""),
                $(".private_message").html(d ? d: "")
            }
        }
    })
});