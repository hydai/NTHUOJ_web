for i in * ; do
    if [ -d "$i" ]; then
        pylint "$i"
    fi
done
