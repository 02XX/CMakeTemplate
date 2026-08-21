function(project_set_warnings target)
    if(NOT TARGET "${target}")
        message(FATAL_ERROR "project_set_warnings: '${target}' is not a CMake target")
    endif()

    set(msvc_warnings
        /W4
        /permissive-
        /w14242
        /w14254
        /w14263
        /w14265
        /w14287
        /we4289
        /w14296
        /w14311
        /w14545
        /w14546
        /w14547
        /w14549
        /w14555
        /w14619
        /w14640
        /w14826
        /w14905
        /w14906
        /w14928
    )

    set(clang_warnings
        -Wall
        -Wextra
        -Wshadow
        -Wnon-virtual-dtor
        -Wold-style-cast
        -Wcast-align
        -Wunused
        -Woverloaded-virtual
        -Wpedantic
        -Wconversion
        -Wsign-conversion
        -Wnull-dereference
        -Wdouble-promotion
        -Wformat=2
        -Wimplicit-fallthrough
    )

    set(gcc_warnings
        ${clang_warnings}
        -Wmisleading-indentation
        -Wduplicated-cond
        -Wduplicated-branches
        -Wlogical-op
        -Wuseless-cast
    )

    if(MSVC)
        set(warnings ${msvc_warnings})
    elseif(CMAKE_CXX_COMPILER_ID MATCHES ".*Clang")
        set(warnings ${clang_warnings})
    elseif(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
        set(warnings ${gcc_warnings})
    else()
        message(WARNING "No compiler warnings configured for '${CMAKE_CXX_COMPILER_ID}'")
        return()
    endif()

    get_target_property(target_type "${target}" TYPE)
    if(target_type STREQUAL "INTERFACE_LIBRARY")
        target_compile_options("${target}" INTERFACE ${warnings})
    else()
        target_compile_options("${target}" PRIVATE ${warnings})
    endif()
endfunction()
