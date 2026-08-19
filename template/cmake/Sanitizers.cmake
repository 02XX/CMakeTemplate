function(project_enable_sanitizers target)
    if(NOT TARGET "${target}")
        message(FATAL_ERROR "project_enable_sanitizers: '${target}' is not a CMake target")
    endif()

    if(NOT CMAKE_CXX_COMPILER_ID MATCHES "GNU|.*Clang")
        return()
    endif()

    set(sanitizers "")

    if(ENABLE_SANITIZER_ADDRESS)
        list(APPEND sanitizers address)
    endif()

    if(ENABLE_SANITIZER_UNDEFINED)
        list(APPEND sanitizers undefined)
    endif()

    if(ENABLE_SANITIZER_LEAK)
        list(APPEND sanitizers leak)
    endif()

    if(ENABLE_SANITIZER_THREAD)
        if(ENABLE_SANITIZER_ADDRESS OR ENABLE_SANITIZER_LEAK)
            message(WARNING "Thread sanitizer is incompatible with address/leak sanitizers; skipping thread sanitizer")
        else()
            list(APPEND sanitizers thread)
        endif()
    endif()

    if(sanitizers STREQUAL "")
        return()
    endif()

    list(JOIN sanitizers "," sanitizer_list)

    get_target_property(target_type "${target}" TYPE)
    if(target_type STREQUAL "INTERFACE_LIBRARY")
        set(visibility INTERFACE)
    else()
        set(visibility PRIVATE)
    endif()

    target_compile_options("${target}" ${visibility} -fsanitize=${sanitizer_list} -fno-omit-frame-pointer)
    target_link_options("${target}" ${visibility} -fsanitize=${sanitizer_list})
endfunction()
